import hashlib

from sqlalchemy import (
    func,
    select,
)

from sqlalchemy.exc import (
    IntegrityError,
)

from sqlalchemy.orm import Session

from app.models.participante import (
    Participante,
)

from app.models.votacion_publica_config import (
    VotacionPublicaConfig,
)

from app.models.voto_publico import (
    VotoPublico,
)

from app.schemas.voto_publico import (
    VotoPublicoCreate,
)


def generar_hash(
    valor: str | None
) -> str | None:

    if not valor:
        return None

    return hashlib.sha256(
        valor.encode(
            "utf-8"
        )
    ).hexdigest()


def obtener_configuracion(
    db: Session
) -> VotacionPublicaConfig | None:

    return db.get(
        VotacionPublicaConfig,
        1
    )


def registrar_voto(
    db: Session,
    data: VotoPublicoCreate,
    ip: str | None,
    user_agent: str | None
) -> VotoPublico:

    config = obtener_configuracion(
        db=db
    )

    if (
        not config
        or
        not config.activa
    ):

        raise ValueError(
            "La votación pública "
            "no se encuentra habilitada."
        )

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
            "El participante no se "
            "encuentra activo."
        )

    if (
        not participante
        .habilitado_votacion_publica
    ):

        raise ValueError(
            "Este participante no "
            "se encuentra habilitado "
            "para la votación pública."
        )

    voto_existente = db.scalar(
        select(VotoPublico)
        .where(
            VotoPublico
            .identificador_votante
            ==
            data.identificador_votante
        )
    )

    if voto_existente:

        raise ValueError(
            "Este dispositivo ya "
            "registró un voto."
        )

    ip_hash = generar_hash(
        ip
    )

    user_agent_hash = generar_hash(
        user_agent
    )

    voto = VotoPublico(
        participante_id=
            data.participante_id,

        identificador_votante=
            data.identificador_votante,

        ip_hash=
            ip_hash,

        user_agent_hash=
            user_agent_hash
    )

    try:

        db.add(voto)

        db.commit()

        db.refresh(voto)

        return voto

    except IntegrityError:

        db.rollback()

        raise ValueError(
            "No fue posible registrar "
            "el voto porque ya existe "
            "un voto asociado."
        )

    except Exception:

        db.rollback()

        raise


def listar_participantes_publicos(
    db: Session
) -> list[Participante]:

    config = obtener_configuracion(
        db=db
    )

    if (
        not config
        or
        not config.activa
    ):

        return []

    query = (
        select(Participante)
        .where(
            Participante.activo
            .is_(True),

            Participante
            .habilitado_votacion_publica
            .is_(True)
        )
        .order_by(
            Participante.codigo
        )
    )

    return list(
        db.scalars(
            query
        ).all()
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
            ).label(
                "total_votos"
            )
        )
        .outerjoin(
            VotoPublico,

            VotoPublico.participante_id
            ==
            Participante.id
        )
        .where(
            Participante
            .habilitado_votacion_publica
            .is_(True)
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