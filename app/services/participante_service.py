from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.participante import Participante
from app.schemas.participante import (
    ParticipanteCreate,
    ParticipanteUpdate,
)


def crear_participante(
    db: Session,
    data: ParticipanteCreate
) -> Participante:

    existente = db.scalar(
        select(Participante).where(
            Participante.codigo == data.codigo
        )
    )

    if existente:
        raise ValueError(
            "Ya existe un participante con este código."
        )

    participante = Participante(
        codigo=data.codigo,
        nombre=data.nombre,
        programa_doctoral=data.programa_doctoral,
        titulo_presentacion=data.titulo_presentacion,
        imagen_s3_key=data.imagen_s3_key,
        activo=True
    )

    db.add(participante)
    db.commit()
    db.refresh(participante)

    return participante


def listar_participantes(
    db: Session,
    solo_activos: bool = True
) -> list[Participante]:

    query = select(Participante)

    if solo_activos:
        query = query.where(
            Participante.activo.is_(True)
        )

    query = query.order_by(
        Participante.nombre
    )

    return list(
        db.scalars(query).all()
    )


def obtener_participante(
    db: Session,
    participante_id: int
) -> Participante | None:

    return db.get(
        Participante,
        participante_id
    )


def actualizar_participante(
    db: Session,
    participante: Participante,
    data: ParticipanteUpdate
) -> Participante:

    cambios = data.model_dump(
        exclude_unset=True
    )

    if "codigo" in cambios:

        existente = db.scalar(
            select(Participante).where(
                Participante.codigo == cambios["codigo"],
                Participante.id != participante.id
            )
        )

        if existente:
            raise ValueError(
                "Ya existe otro participante con este código."
            )

    for campo, valor in cambios.items():
        setattr(
            participante,
            campo,
            valor
        )

    db.commit()
    db.refresh(participante)

    return participante


def eliminar_participante(
    db: Session,
    participante: Participante
) -> Participante:

    participante.activo = False

    db.commit()
    db.refresh(participante)

    return participante