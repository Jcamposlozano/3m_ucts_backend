import hashlib

from sqlalchemy import (
    func,
    select,
)

from sqlalchemy.orm import Session

from app.models.participante import Participante
from app.models.voto_publico import VotoPublico

from app.schemas.voto_publico import (
    VotoPublicoCreate,
)


def generar_hash(
    valor: str | None
) -> str | None:

    if not valor:
        return None

    return hashlib.sha256(
        valor.encode("utf-8")
    ).hexdigest()


def registrar_voto(
    db: Session,
    data: VotoPublicoCreate,
    ip: str | None,
    user_agent: str | None
) -> VotoPublico:

    # -----------------------------------------------------
    # 1. Validar participante
    # -----------------------------------------------------

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
            "El participante no se encuentra habilitado."
        )

    # -----------------------------------------------------
    # 2. Validar identificador del votante
    # -----------------------------------------------------

    voto_existente = db.scalar(
        select(VotoPublico).where(
            VotoPublico.identificador_votante
            == data.identificador_votante
        )
    )

    if voto_existente:
        raise ValueError(
            "Este dispositivo ya registró un voto."
        )

    # -----------------------------------------------------
    # 3. Generar hashes
    # -----------------------------------------------------

    ip_hash = generar_hash(ip)

    user_agent_hash = generar_hash(
        user_agent
    )

    # -----------------------------------------------------
    # 4. Crear voto
    # -----------------------------------------------------

    voto = VotoPublico(
        participante_id=data.participante_id,

        identificador_votante=(
            data.identificador_votante
        ),

        ip_hash=ip_hash,

        user_agent_hash=user_agent_hash
    )

    try:

        db.add(voto)
        db.commit()
        db.refresh(voto)

        return voto

    except Exception:

        db.rollback()
        raise


def listar_participantes_publicos(
    db: Session
) -> list[Participante]:

    query = (
        select(Participante)
        .where(
            Participante.activo.is_(True)
        )
        .order_by(
            Participante.codigo
        )
    )

    return list(
        db.scalars(query).all()
    )


def obtener_resultados(
    db: Session
):

    query = (
        select(
            Participante.id,
            Participante.codigo,
            Participante.nombre,
            func.count(
                VotoPublico.id
            ).label("total_votos")
        )
        .outerjoin(
            VotoPublico,
            VotoPublico.participante_id
            == Participante.id
        )
        .where(
            Participante.activo.is_(True)
        )
        .group_by(
            Participante.id,
            Participante.codigo,
            Participante.nombre
        )
        .order_by(
            func.count(
                VotoPublico.id
            ).desc()
        )
    )

    return db.execute(
        query
    ).all()