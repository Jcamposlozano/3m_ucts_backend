from datetime import datetime

from sqlalchemy import (
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


class Evaluacion(Base):
    __tablename__ = "evaluacion"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    jurado_id: Mapped[int] = mapped_column(
        ForeignKey("jurado.id"),
        nullable=False,
        index=True
    )

    participante_id: Mapped[int] = mapped_column(
        ForeignKey("participante.id"),
        nullable=False,
        index=True
    )

    rubrica_id: Mapped[int] = mapped_column(
        ForeignKey("rubrica.id"),
        nullable=False,
        index=True
    )

    estado: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="PENDIENTE"
    )

    puntaje_total: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    aspecto_positivo: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    aspecto_por_mejorar: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    firma_s3_key: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    pdf_s3_key: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    pdf_hash: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    fecha_asignacion: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    fecha_inicio: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    fecha_finalizacion: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
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
            "jurado_id",
            "participante_id",
            "rubrica_id",
            name="uq_jurado_participante_rubrica"
        ),
    )