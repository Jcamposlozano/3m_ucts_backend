from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.jurado import (
    JuradoCreate,
    JuradoResponse,
    JuradoUpdate,
)

from app.schemas.participante_estado import (
    ParticipanteEstadoResponse,
)

from app.services.jurado_service import (
    actualizar_jurado,
    crear_jurado,
    eliminar_jurado,
    listar_jurados,
    obtener_jurado,
)

from app.services.jurado_participante_service import (
    listar_participantes_por_jurado,
)


router = APIRouter(
    prefix="/api/jurados",
    tags=["Jurados"]
)


@router.post(
    "",
    response_model=JuradoResponse,
    status_code=status.HTTP_201_CREATED
)
def crear(
    data: JuradoCreate,
    db: Session = Depends(get_db)
):

    try:
        return crear_jurado(
            db=db,
            data=data
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc)
        )


@router.get(
    "",
    response_model=list[JuradoResponse]
)
def listar(
    solo_activos: bool = Query(
        default=True
    ),
    db: Session = Depends(get_db)
):

    return listar_jurados(
        db=db,
        solo_activos=solo_activos
    )


@router.get(
    "/{jurado_id}",
    response_model=JuradoResponse
)
def obtener(
    jurado_id: int,
    db: Session = Depends(get_db)
):

    jurado = obtener_jurado(
        db=db,
        jurado_id=jurado_id
    )

    if not jurado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jurado no encontrado."
        )

    return jurado


@router.get(
    "/{jurado_id}/participantes",
    response_model=list[ParticipanteEstadoResponse]
)
def participantes_del_jurado(
    jurado_id: int,
    rubrica_id: int = Query(...),
    db: Session = Depends(get_db)
):

    try:

        return listar_participantes_por_jurado(
            db=db,
            jurado_id=jurado_id,
            rubrica_id=rubrica_id
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc)
        )


@router.patch(
    "/{jurado_id}",
    response_model=JuradoResponse
)
def actualizar(
    jurado_id: int,
    data: JuradoUpdate,
    db: Session = Depends(get_db)
):

    jurado = obtener_jurado(
        db=db,
        jurado_id=jurado_id
    )

    if not jurado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jurado no encontrado."
        )

    try:

        return actualizar_jurado(
            db=db,
            jurado=jurado,
            data=data
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc)
        )


@router.delete(
    "/{jurado_id}",
    response_model=JuradoResponse
)
def eliminar(
    jurado_id: int,
    db: Session = Depends(get_db)
):

    jurado = obtener_jurado(
        db=db,
        jurado_id=jurado_id
    )

    if not jurado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jurado no encontrado."
        )

    if not jurado.activo:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El jurado ya se encuentra inactivo."
        )

    return eliminar_jurado(
        db=db,
        jurado=jurado
    )