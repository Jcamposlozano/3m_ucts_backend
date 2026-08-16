from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Criterio(Base):
    __tablename__ = "criterio"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    rubrica_id: Mapped[int] = mapped_column(
        ForeignKey("rubrica.id"),
        nullable=False,
        index=True
    )

    codigo: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    categoria: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    titulo: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    descripcion: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    orden: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    puntaje_minimo: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.5
    )

    puntaje_maximo: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=5.0
    )

    incremento: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.5
    )

    activo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    __table_args__ = (
        UniqueConstraint(
            "rubrica_id",
            "codigo",
            name="uq_rubrica_codigo"
        ),
    )