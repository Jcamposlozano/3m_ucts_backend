from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.admin_votacion import (
    EstadoVotacionPublicaResponse,
    SeleccionarParticipantesVotacion,
)

from app.services.admin_votacion_service import (
    abrir_votacion,
    cerrar_votacion,
    obtener_estado_votacion,
    seleccionar_participantes,
)


router = APIRouter(
    prefix="/api/admin/votacion-publica",
    tags=[
        "Administración - Votación pública"
    ]
)


@router.get(
    "",
    response_model=
        EstadoVotacionPublicaResponse
)
def obtener_estado(
    db: Session = Depends(get_db)
):

    return obtener_estado_votacion(
        db=db
    )


@router.put(
    "/participantes",
    response_model=
        EstadoVotacionPublicaResponse
)
def configurar_participantes(
    data:
        SeleccionarParticipantesVotacion,

    db: Session = Depends(get_db)
):

    try:

        return seleccionar_participantes(
            db=db,
            participantes_ids=
                data.participantes_ids
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=
                status.HTTP_409_CONFLICT,

            detail=
                str(exc)
        )


@router.post(
    "/abrir",
    response_model=
        EstadoVotacionPublicaResponse
)
def abrir(
    db: Session = Depends(get_db)
):

    try:

        return abrir_votacion(
            db=db
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=
                status.HTTP_409_CONFLICT,

            detail=
                str(exc)
        )


@router.post(
    "/cerrar",
    response_model=
        EstadoVotacionPublicaResponse
)
def cerrar(
    db: Session = Depends(get_db)
):

    try:

        return cerrar_votacion(
            db=db
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=
                status.HTTP_409_CONFLICT,

            detail=
                str(exc)
        )