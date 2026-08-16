from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database import Base


class Participante(Base):

    __tablename__ = "participante"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )


    codigo: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
        index=True,
    )


    nombre: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )


    programa_doctoral: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )


    titulo_presentacion: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )


    imagen_s3_key: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )


    activo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )


    habilitado_votacion_publica: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )


    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )