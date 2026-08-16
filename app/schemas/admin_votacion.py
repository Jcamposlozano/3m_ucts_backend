from datetime import datetime

from pydantic import BaseModel


class ParticipanteVotacionResponse(BaseModel):
    id: int
    codigo: str
    nombre: str
    activo: bool
    habilitado_votacion_publica: bool


class SeleccionarParticipantesVotacion(BaseModel):
    participantes_ids: list[int]


class EstadoVotacionPublicaResponse(BaseModel):
    activa: bool

    fecha_apertura: datetime | None
    fecha_cierre: datetime | None

    participantes_habilitados: list[
        ParticipanteVotacionResponse
    ]