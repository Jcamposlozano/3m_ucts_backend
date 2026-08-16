from pydantic import BaseModel


class CriterioRubricaResponse(BaseModel):
    id: int
    codigo: str
    categoria: str | None
    titulo: str
    descripcion: str | None
    orden: int
    puntaje_minimo: float
    puntaje_maximo: float
    incremento: float


class RubricaResponse(BaseModel):
    id: int
    codigo: str
    nombre: str
    version: int
    descripcion: str | None
    puntaje_maximo: float
    activa: bool
    criterios: list[CriterioRubricaResponse]