from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class VotoPublicoCreate(BaseModel):

    participante_id: int

    identificador_votante: str = Field(
        min_length=10,
        max_length=255
    )


class VotoPublicoResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    participante_id: int
    fecha_voto: datetime


class ParticipantePublicoResponse(BaseModel):

    id: int
    codigo: str
    nombre: str
    programa_doctoral: str | None
    titulo_presentacion: str
    imagen_s3_key: str | None


class ResultadoPublicoResponse(BaseModel):

    participante_id: int
    codigo: str
    nombre: str
    total_votos: int