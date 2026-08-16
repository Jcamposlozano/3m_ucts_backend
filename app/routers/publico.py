from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    status,
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.voto_publico import (
    ParticipantePublicoResponse,
    ResultadoPublicoResponse,
    VotoPublicoCreate,
    VotoPublicoResponse,
)

from app.services.voto_publico_service import (
    listar_participantes_publicos,
    obtener_resultados,
    registrar_voto,
)

from app.services.resultados_realtime_service import (
    emitir_resultados_actualizados,
)


router = APIRouter(
    prefix="/api/publico",
    tags=["Votación pública"],
)


# =========================================================
# LISTAR PARTICIPANTES PARA EL TARJETÓN
# =========================================================

@router.get(
    "/participantes",
    response_model=list[ParticipantePublicoResponse],
)
def participantes(
    db: Session = Depends(get_db),
):

    return listar_participantes_publicos(
        db=db
    )


# =========================================================
# REGISTRAR VOTO
# =========================================================

@router.post(
    "/votos",
    response_model=VotoPublicoResponse,
    status_code=status.HTTP_201_CREATED,
)
async def votar(
    data: VotoPublicoCreate,
    request: Request,
    db: Session = Depends(get_db),
):

    ip = None

    if request.client:
        ip = request.client.host

    user_agent = request.headers.get(
        "user-agent"
    )

    try:

        voto = registrar_voto(
            db=db,
            data=data,
            ip=ip,
            user_agent=user_agent,
        )

        # -------------------------------------------------
        # ACTUALIZAR RESULTADOS EN TIEMPO REAL
        # -------------------------------------------------

        await emitir_resultados_actualizados(
            db=db
        )

        return voto

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )


# =========================================================
# RESULTADOS PÚBLICOS
# =========================================================

@router.get(
    "/resultados",
    response_model=list[ResultadoPublicoResponse],
)
def resultados(
    db: Session = Depends(get_db),
):

    registros = obtener_resultados(
        db=db
    )

    return [
        ResultadoPublicoResponse(
            participante_id=registro.id,
            codigo=registro.codigo,
            nombre=registro.nombre,
            total_votos=registro.total_votos,
        )
        for registro in registros
    ]