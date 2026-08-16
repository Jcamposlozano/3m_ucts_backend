from pydantic import BaseModel


class ParticipanteEstadoResponse(BaseModel):
    id: int
    codigo: str
    nombre: str
    programa_doctoral: str | None
    titulo_presentacion: str
    imagen_s3_key: str | None

    evaluado: bool

    evaluacion_id: int | None
    estado_evaluacion: str | None
    puntaje_total: float | None