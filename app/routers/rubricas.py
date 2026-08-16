from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.criterio import Criterio
from app.models.rubrica import Rubrica

from app.schemas.rubrica import (
    CriterioRubricaResponse,
    RubricaResponse,
)


router = APIRouter(
    prefix="/api/rubricas",
    tags=["Rúbricas"]
)


@router.get(
    "/{rubrica_id}",
    response_model=RubricaResponse
)
def obtener_rubrica(
    rubrica_id: int,
    db: Session = Depends(get_db)
):

    rubrica = db.get(
        Rubrica,
        rubrica_id
    )

    if not rubrica:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rúbrica no encontrada."
        )

    criterios = list(
        db.scalars(
            select(Criterio)
            .where(
                Criterio.rubrica_id == rubrica_id,
                Criterio.activo.is_(True)
            )
            .order_by(
                Criterio.orden
            )
        ).all()
    )

    return RubricaResponse(
        id=rubrica.id,
        codigo=rubrica.codigo,
        nombre=rubrica.nombre,
        version=rubrica.version,
        descripcion=rubrica.descripcion,
        puntaje_maximo=rubrica.puntaje_maximo,
        activa=rubrica.activa,
        criterios=[
            CriterioRubricaResponse(
                id=criterio.id,
                codigo=criterio.codigo,
                categoria=criterio.categoria,
                titulo=criterio.titulo,
                descripcion=criterio.descripcion,
                orden=criterio.orden,
                puntaje_minimo=criterio.puntaje_minimo,
                puntaje_maximo=criterio.puntaje_maximo,
                incremento=criterio.incremento
            )
            for criterio in criterios
        ]
    )