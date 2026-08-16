from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ParticipanteCreate(BaseModel):
    codigo: str = Field(
        min_length=1,
        max_length=50
    )

    nombre: str = Field(
        min_length=1,
        max_length=200
    )

    programa_doctoral: str | None = None

    titulo_presentacion: str = Field(
        min_length=1
    )

    imagen_s3_key: str | None = None


class ParticipanteUpdate(BaseModel):
    codigo: str | None = Field(
        default=None,
        min_length=1,
        max_length=50
    )

    nombre: str | None = Field(
        default=None,
        min_length=1,
        max_length=200
    )

    programa_doctoral: str | None = None

    titulo_presentacion: str | None = None

    imagen_s3_key: str | None = None

    activo: bool | None = None


class ParticipanteResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    codigo: str
    nombre: str
    programa_doctoral: str | None
    titulo_presentacion: str
    imagen_s3_key: str | None
    activo: bool
    created_at: datetime
    updated_at: datetime