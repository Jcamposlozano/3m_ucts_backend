from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.evaluacion import Evaluacion
from app.models.jurado import Jurado
from app.models.participante import Participante


def listar_participantes_por_jurado(
    db: Session,
    jurado_id: int,
    rubrica_id: int
):

    jurado = db.get(
        Jurado,
        jurado_id
    )

    if not jurado:
        raise ValueError(
            "El jurado no existe."
        )

    if not jurado.activo:
        raise ValueError(
            "El jurado se encuentra inactivo."
        )

    participantes = list(
        db.scalars(
            select(Participante)
            .where(
                Participante.activo.is_(True)
            )
            .order_by(
                Participante.codigo
            )
        ).all()
    )

    evaluaciones = list(
        db.scalars(
            select(Evaluacion).where(
                Evaluacion.jurado_id == jurado_id,
                Evaluacion.rubrica_id == rubrica_id
            )
        ).all()
    )

    evaluaciones_por_participante = {
        evaluacion.participante_id: evaluacion
        for evaluacion in evaluaciones
    }

    resultado = []

    for participante in participantes:

        evaluacion = evaluaciones_por_participante.get(
            participante.id
        )

        resultado.append(
            {
                "id": participante.id,
                "codigo": participante.codigo,
                "nombre": participante.nombre,
                "programa_doctoral": participante.programa_doctoral,
                "titulo_presentacion": participante.titulo_presentacion,
                "imagen_s3_key": participante.imagen_s3_key,

                "evaluado": (
                    evaluacion is not None
                    and evaluacion.estado == "FINALIZADA"
                ),

                "evaluacion_id": (
                    evaluacion.id
                    if evaluacion
                    else None
                ),

                "estado_evaluacion": (
                    evaluacion.estado
                    if evaluacion
                    else None
                ),

                "puntaje_total": (
                    evaluacion.puntaje_total
                    if evaluacion
                    else None
                )
            }
        )

    return resultado