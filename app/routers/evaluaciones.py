from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.evaluacion import Evaluacion
from app.models.respuesta_evaluacion import RespuestaEvaluacion

from app.schemas.evaluacion import (
    EvaluacionCreate,
    EvaluacionDetalleResponse,
    EvaluacionResponse,
    RespuestaEvaluacionResponse,
)

from app.services.evaluacion_service import (
    crear_evaluacion,
)


router = APIRouter(
    prefix="/api/evaluaciones",
    tags=["Evaluaciones"]
)


@router.post(
    "",
    response_model=EvaluacionResponse,
    status_code=status.HTTP_201_CREATED
)
def crear(
    data: EvaluacionCreate,
    db: Session = Depends(get_db)
):

    try:

        return crear_evaluacion(
            db=db,
            data=data
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc)
        )


@router.get(
    "/{evaluacion_id}",
    response_model=EvaluacionDetalleResponse
)
def obtener(
    evaluacion_id: int,
    db: Session = Depends(get_db)
):

    evaluacion = db.get(
        Evaluacion,
        evaluacion_id
    )

    if not evaluacion:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evaluación no encontrada."
        )

    respuestas_db = list(
        db.scalars(
            select(
                RespuestaEvaluacion
            ).where(
                RespuestaEvaluacion.evaluacion_id
                == evaluacion_id
            )
        ).all()
    )

    return EvaluacionDetalleResponse(
        id=evaluacion.id,

        jurado_id=evaluacion.jurado_id,
        participante_id=evaluacion.participante_id,
        rubrica_id=evaluacion.rubrica_id,

        estado=evaluacion.estado,

        puntaje_total=evaluacion.puntaje_total,

        aspecto_positivo=evaluacion.aspecto_positivo,
        aspecto_por_mejorar=evaluacion.aspecto_por_mejorar,

        firma_s3_key=evaluacion.firma_s3_key,
        pdf_s3_key=evaluacion.pdf_s3_key,
        pdf_hash=evaluacion.pdf_hash,

        fecha_inicio=evaluacion.fecha_inicio,
        fecha_finalizacion=evaluacion.fecha_finalizacion,

        created_at=evaluacion.created_at,
        updated_at=evaluacion.updated_at,

        respuestas=[
            RespuestaEvaluacionResponse(
                criterio_id=respuesta.criterio_id,
                puntaje=respuesta.puntaje
            )
            for respuesta in respuestas_db
        ]
    )


@router.get(
    "/jurado/{jurado_id}",
    response_model=list[EvaluacionResponse]
)
def listar_por_jurado(
    jurado_id: int,
    db: Session = Depends(get_db)
):

    evaluaciones = list(
        db.scalars(
            select(Evaluacion)
            .where(
                Evaluacion.jurado_id == jurado_id
            )
            .order_by(
                Evaluacion.created_at.desc()
            )
        ).all()
    )

    return evaluaciones