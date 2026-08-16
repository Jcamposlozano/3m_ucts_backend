from pydantic import BaseModel


class ResultadoJuradoDetalle(BaseModel):
    jurado_id: int
    nombre: str
    puntaje: float
    evaluacion_id: int


class ResultadoParticipante(BaseModel):
    ranking: int | None

    participante_id: int
    codigo: str
    nombre: str

    programa_doctoral: str | None
    titulo_presentacion: str

    cantidad_evaluaciones: int

    promedio: float | None

    jurados: list[ResultadoJuradoDetalle]

    votos_publicos: int


class ResultadoJuradoHeader(BaseModel):
    id: int
    nombre: str


class ResultadosAdminResponse(BaseModel):
    total_participantes: int

    total_evaluaciones_finalizadas: int

    total_votos_publicos: int

    jurados: list[ResultadoJuradoHeader]

    resultados: list[ResultadoParticipante]