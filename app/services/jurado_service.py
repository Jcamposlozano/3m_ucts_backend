from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.jurado import Jurado
from app.schemas.jurado import (
    JuradoCreate,
    JuradoUpdate,
)


def crear_jurado(
    db: Session,
    data: JuradoCreate
) -> Jurado:

    condiciones = [
        Jurado.email == data.email
    ]

    if data.cognito_sub:
        condiciones.append(
            Jurado.cognito_sub == data.cognito_sub
        )

    existente = db.scalar(
        select(Jurado).where(
            or_(*condiciones)
        )
    )

    if existente:
        if existente.email == data.email:
            raise ValueError(
                "Ya existe un jurado con este correo electrónico."
            )

        raise ValueError(
            "Ya existe un jurado asociado a este usuario de Cognito."
        )

    jurado = Jurado(
        nombre=data.nombre,
        email=data.email,
        cognito_sub=data.cognito_sub,
        activo=True
    )

    db.add(jurado)
    db.commit()
    db.refresh(jurado)

    return jurado


def listar_jurados(
    db: Session,
    solo_activos: bool = True
) -> list[Jurado]:

    query = select(Jurado)

    if solo_activos:
        query = query.where(
            Jurado.activo.is_(True)
        )

    query = query.order_by(
        Jurado.nombre
    )

    return list(
        db.scalars(query).all()
    )


def obtener_jurado(
    db: Session,
    jurado_id: int
) -> Jurado | None:

    return db.get(
        Jurado,
        jurado_id
    )


def actualizar_jurado(
    db: Session,
    jurado: Jurado,
    data: JuradoUpdate
) -> Jurado:

    cambios = data.model_dump(
        exclude_unset=True
    )

    if "email" in cambios:
        existente = db.scalar(
            select(Jurado).where(
                Jurado.email == cambios["email"],
                Jurado.id != jurado.id
            )
        )

        if existente:
            raise ValueError(
                "Ya existe otro jurado con este correo electrónico."
            )

    if (
        "cognito_sub" in cambios
        and cambios["cognito_sub"] is not None
    ):
        existente = db.scalar(
            select(Jurado).where(
                Jurado.cognito_sub == cambios["cognito_sub"],
                Jurado.id != jurado.id
            )
        )

        if existente:
            raise ValueError(
                "Ya existe otro jurado asociado a este usuario de Cognito."
            )

    for campo, valor in cambios.items():
        setattr(
            jurado,
            campo,
            valor
        )

    db.commit()
    db.refresh(jurado)

    return jurado


def eliminar_jurado(
    db: Session,
    jurado: Jurado
) -> Jurado:

    jurado.activo = False

    db.commit()
    db.refresh(jurado)

    return jurado