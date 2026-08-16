from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database import Base


class VotoPublico(Base):
    __tablename__ = "voto_publico"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    participante_id: Mapped[int] = mapped_column(
        ForeignKey("participante.id"),
        nullable=False,
        index=True
    )

    identificador_votante: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    ip_hash: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    user_agent_hash: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    fecha_voto: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )