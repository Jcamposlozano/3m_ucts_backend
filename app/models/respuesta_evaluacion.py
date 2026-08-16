from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    UniqueConstraint,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database import Base


class RespuestaEvaluacion(Base):
    __tablename__ = "respuesta_evaluacion"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    evaluacion_id: Mapped[int] = mapped_column(
        ForeignKey(
            "evaluacion.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    criterio_id: Mapped[int] = mapped_column(
        ForeignKey(
            "criterio.id"
        ),
        nullable=False,
        index=True
    )

    puntaje: Mapped[float] = mapped_column(
        Float,
        nullable=False
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
            "evaluacion_id",
            "criterio_id",
            name="uq_evaluacion_criterio"
        ),
    )