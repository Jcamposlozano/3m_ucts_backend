from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.resultados import (
    ResultadosAdminResponse,
)

from app.services.resultados_service import (
    obtener_resultados_admin,
)


router = APIRouter(
    prefix="/api/admin",
    tags=["Administración"],
)


@router.get(
    "/resultados",
    response_model=ResultadosAdminResponse,
)
def resultados(
    db: Session = Depends(get_db),
):

    return obtener_resultados_admin(
        db=db
    )