from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.participante import (
    ParticipanteCreate,
    ParticipanteResponse,
    ParticipanteUpdate,
)

from app.services.participante_service import (
    actualizar_participante,
    crear_participante,
    eliminar_participante,
    listar_participantes,
    obtener_participante,
)


router = APIRouter(
    prefix="/api/participantes",
    tags=["Participantes"]
)


@router.post(
    "",
    response_model=ParticipanteResponse,
    status_code=status.HTTP_201_CREATED
)
def crear(
    data: ParticipanteCreate,
    db: Session = Depends(get_db)
):

    try:

        return crear_participante(
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
    response_model=list[ParticipanteResponse]
)
def listar(
    solo_activos: bool = Query(
        default=True
    ),
    db: Session = Depends(get_db)
):

    return listar_participantes(
        db=db,
        solo_activos=solo_activos
    )


@router.get(
    "/{participante_id}",
    response_model=ParticipanteResponse
)
def obtener(
    participante_id: int,
    db: Session = Depends(get_db)
):

    participante = obtener_participante(
        db=db,
        participante_id=participante_id
    )

    if not participante:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participante no encontrado."
        )

    return participante


@router.patch(
    "/{participante_id}",
    response_model=ParticipanteResponse
)
def actualizar(
    participante_id: int,
    data: ParticipanteUpdate,
    db: Session = Depends(get_db)
):

    participante = obtener_participante(
        db=db,
        participante_id=participante_id
    )

    if not participante:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participante no encontrado."
        )

    try:

        return actualizar_participante(
            db=db,
            participante=participante,
            data=data
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc)
        )


@router.delete(
    "/{participante_id}",
    response_model=ParticipanteResponse
)
def eliminar(
    participante_id: int,
    db: Session = Depends(get_db)
):

    participante = obtener_participante(
        db=db,
        participante_id=participante_id
    )

    if not participante:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participante no encontrado."
        )

    if not participante.activo:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El participante ya se encuentra inactivo."
        )

    return eliminar_participante(
        db=db,
        participante=participante
    )