from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RespuestaEvaluacionCreate(BaseModel):
    criterio_id: int

    puntaje: float = Field(
        ge=0
    )


class EvaluacionCreate(BaseModel):
    jurado_id: int
    participante_id: int
    rubrica_id: int

    respuestas: list[RespuestaEvaluacionCreate]

    aspecto_positivo: str | None = None
    aspecto_por_mejorar: str | None = None


class RespuestaEvaluacionResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    criterio_id: int
    puntaje: float


class EvaluacionResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    jurado_id: int
    participante_id: int
    rubrica_id: int

    estado: str

    puntaje_total: float | None

    aspecto_positivo: str | None
    aspecto_por_mejorar: str | None

    firma_s3_key: str | None
    pdf_s3_key: str | None
    pdf_hash: str | None

    fecha_inicio: datetime | None
    fecha_finalizacion: datetime | None

    created_at: datetime
    updated_at: datetime


class EvaluacionDetalleResponse(EvaluacionResponse):
    respuestas: list[RespuestaEvaluacionResponse]