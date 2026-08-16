from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database import Base


class VotacionPublicaConfig(Base):
    __tablename__ = "votacion_publica_config"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    activa: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    fecha_apertura: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    fecha_cierre: Mapped[datetime | None] = mapped_column(
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