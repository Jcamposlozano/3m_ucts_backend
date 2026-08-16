from datetime import datetime

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.criterio import Criterio
from app.models.evaluacion import Evaluacion
from app.models.jurado import Jurado
from app.models.participante import Participante
from app.models.respuesta_evaluacion import RespuestaEvaluacion
from app.models.rubrica import Rubrica

from app.schemas.evaluacion import EvaluacionCreate


def crear_evaluacion(
    db: Session,
    data: EvaluacionCreate
) -> Evaluacion:

    # ---------------------------------------------------------
    # 1. Validar jurado
    # ---------------------------------------------------------

    jurado = db.get(
        Jurado,
        data.jurado_id
    )

    if not jurado:
        raise ValueError(
            "El jurado no existe."
        )

    if not jurado.activo:
        raise ValueError(
            "El jurado se encuentra inactivo."
        )

    # ---------------------------------------------------------
    # 2. Validar participante
    # ---------------------------------------------------------

    participante = db.get(
        Participante,
        data.participante_id
    )

    if not participante:
        raise ValueError(
            "El participante no existe."
        )

    if not participante.activo:
        raise ValueError(
            "El participante se encuentra inactivo."
        )

    # ---------------------------------------------------------
    # 3. Validar rúbrica
    # ---------------------------------------------------------

    rubrica = db.get(
        Rubrica,
        data.rubrica_id
    )

    if not rubrica:
        raise ValueError(
            "La rúbrica no existe."
        )

    if not rubrica.activa:
        raise ValueError(
            "La rúbrica se encuentra inactiva."
        )

    # ---------------------------------------------------------
    # 4. Verificar si ya existe evaluación
    # ---------------------------------------------------------

    evaluacion_existente = db.scalar(
        select(Evaluacion).where(
            Evaluacion.jurado_id == data.jurado_id,
            Evaluacion.participante_id == data.participante_id,
            Evaluacion.rubrica_id == data.rubrica_id
        )
    )

    if evaluacion_existente:
        raise ValueError(
            "Este participante ya fue evaluado por este jurado."
        )

    # ---------------------------------------------------------
    # 5. Obtener criterios activos de la rúbrica
    # ---------------------------------------------------------

    criterios = list(
        db.scalars(
            select(Criterio)
            .where(
                Criterio.rubrica_id == data.rubrica_id,
                Criterio.activo.is_(True)
            )
            .order_by(Criterio.orden)
        ).all()
    )

    if not criterios:
        raise ValueError(
            "La rúbrica no tiene criterios activos."
        )

    # ---------------------------------------------------------
    # 6. Validar cantidad de respuestas
    # ---------------------------------------------------------

    if len(data.respuestas) != len(criterios):
        raise ValueError(
            "Debe responder todos los criterios de la rúbrica."
        )

    criterios_por_id = {
        criterio.id: criterio
        for criterio in criterios
    }

    ids_recibidos = [
        respuesta.criterio_id
        for respuesta in data.respuestas
    ]

    # No permitir mismo criterio dos veces
    if len(ids_recibidos) != len(set(ids_recibidos)):
        raise ValueError(
            "Existen criterios duplicados en la evaluación."
        )

    # ---------------------------------------------------------
    # 7. Validar cada respuesta
    # ---------------------------------------------------------

    puntaje_total = 0.0

    for respuesta in data.respuestas:

        criterio = criterios_por_id.get(
            respuesta.criterio_id
        )

        if not criterio:
            raise ValueError(
                f"El criterio {respuesta.criterio_id} "
                "no pertenece a la rúbrica seleccionada."
            )

        puntaje = respuesta.puntaje

        if (
            puntaje < criterio.puntaje_minimo
            or puntaje > criterio.puntaje_maximo
        ):
            raise ValueError(
                f"El puntaje del criterio {criterio.codigo} "
                f"debe estar entre "
                f"{criterio.puntaje_minimo} y "
                f"{criterio.puntaje_maximo}."
            )

        diferencia = (
            puntaje - criterio.puntaje_minimo
        )

        division = (
            diferencia / criterio.incremento
        )

        if abs(
            division - round(division)
        ) > 1e-9:
            raise ValueError(
                f"El puntaje del criterio {criterio.codigo} "
                f"debe avanzar en incrementos de "
                f"{criterio.incremento}."
            )

        puntaje_total += puntaje

    puntaje_total = round(
        puntaje_total,
        2
    )

    # ---------------------------------------------------------
    # 8. Validar máximo de la rúbrica
    # ---------------------------------------------------------

    if puntaje_total > rubrica.puntaje_maximo:
        raise ValueError(
            "El puntaje total supera el máximo permitido "
            "por la rúbrica."
        )

    # ---------------------------------------------------------
    # 9. Crear evaluación
    # ---------------------------------------------------------

    ahora = datetime.utcnow()

    evaluacion = Evaluacion(
        jurado_id=data.jurado_id,
        participante_id=data.participante_id,
        rubrica_id=data.rubrica_id,

        estado="FINALIZADA",

        puntaje_total=puntaje_total,

        aspecto_positivo=data.aspecto_positivo,
        aspecto_por_mejorar=data.aspecto_por_mejorar,

        fecha_inicio=ahora,
        fecha_finalizacion=ahora
    )

    try:

        db.add(evaluacion)

        # Necesitamos el ID antes de crear respuestas
        db.flush()

        # -----------------------------------------------------
        # 10. Crear respuestas
        # -----------------------------------------------------

        for respuesta in data.respuestas:

            nueva_respuesta = RespuestaEvaluacion(
                evaluacion_id=evaluacion.id,
                criterio_id=respuesta.criterio_id,
                puntaje=respuesta.puntaje
            )

            db.add(
                nueva_respuesta
            )

        # -----------------------------------------------------
        # 11. Commit único
        # -----------------------------------------------------

        db.commit()

        db.refresh(
            evaluacion
        )

        return evaluacion

    except IntegrityError:

        db.rollback()

        raise ValueError(
            "No fue posible registrar la evaluación. "
            "Es posible que el jurado ya haya evaluado "
            "este participante."
        )

    except Exception:

        db.rollback()

        raise