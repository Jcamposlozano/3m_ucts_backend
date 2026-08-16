from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.participante import Participante

from app.models.votacion_publica_config import (
    VotacionPublicaConfig,
)


def obtener_configuracion(
    db: Session
) -> VotacionPublicaConfig:

    config = db.get(
        VotacionPublicaConfig,
        1
    )

    if config:
        return config

    config = VotacionPublicaConfig(
        id=1,
        activa=False
    )

    db.add(config)
    db.commit()
    db.refresh(config)

    return config


def obtener_estado_votacion(
    db: Session
):

    config = obtener_configuracion(
        db=db
    )

    participantes = list(
        db.scalars(
            select(Participante)
            .where(
                Participante
                .habilitado_votacion_publica
                .is_(True)
            )
            .order_by(
                Participante.codigo
            )
        ).all()
    )

    return {
        "activa":
            config.activa,

        "fecha_apertura":
            config.fecha_apertura,

        "fecha_cierre":
            config.fecha_cierre,

        "participantes_habilitados": [
            {
                "id":
                    participante.id,

                "codigo":
                    participante.codigo,

                "nombre":
                    participante.nombre,

                "activo":
                    participante.activo,

                "habilitado_votacion_publica":
                    participante
                    .habilitado_votacion_publica
            }
            for participante
            in participantes
        ]
    }


def seleccionar_participantes(
    db: Session,
    participantes_ids: list[int]
):

    if not participantes_ids:

        raise ValueError(
            "Debe seleccionar al menos "
            "un participante."
        )

    ids_unicos = list(
        set(participantes_ids)
    )

    participantes_seleccionados = list(
        db.scalars(
            select(Participante)
            .where(
                Participante.id.in_(
                    ids_unicos
                )
            )
        ).all()
    )

    if (
        len(participantes_seleccionados)
        != len(ids_unicos)
    ):

        raise ValueError(
            "Uno o más participantes "
            "no existen."
        )

    for participante in (
        participantes_seleccionados
    ):

        if not participante.activo:

            raise ValueError(
                f"El participante "
                f"{participante.codigo} "
                f"se encuentra inactivo."
            )

    todos_los_participantes = list(
        db.scalars(
            select(Participante)
        ).all()
    )

    for participante in (
        todos_los_participantes
    ):

        participante.habilitado_votacion_publica = (
            participante.id
            in ids_unicos
        )

    db.commit()

    return obtener_estado_votacion(
        db=db
    )


def abrir_votacion(
    db: Session
):

    config = obtener_configuracion(
        db=db
    )

    if config.activa:

        raise ValueError(
            "La votación pública "
            "ya se encuentra abierta."
        )

    participantes_habilitados = list(
        db.scalars(
            select(Participante)
            .where(
                Participante.activo.is_(True),

                Participante
                .habilitado_votacion_publica
                .is_(True)
            )
        ).all()
    )

    if (
        len(participantes_habilitados)
        < 2
    ):

        raise ValueError(
            "Debe habilitar al menos "
            "dos participantes antes "
            "de abrir la votación."
        )

    config.activa = True

    config.fecha_apertura = (
        datetime.utcnow()
    )

    config.fecha_cierre = None

    db.commit()
    db.refresh(config)

    return obtener_estado_votacion(
        db=db
    )


def cerrar_votacion(
    db: Session
):

    config = obtener_configuracion(
        db=db
    )

    if not config.activa:

        raise ValueError(
            "La votación pública "
            "ya se encuentra cerrada."
        )

    config.activa = False

    config.fecha_cierre = (
        datetime.utcnow()
    )

    db.commit()
    db.refresh(config)

    return obtener_estado_votacion(
        db=db
    )