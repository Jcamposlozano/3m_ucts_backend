from fastapi import FastAPI

from app.routers.evaluaciones import (
    router as evaluaciones_router
)

from app.routers.jurados import (
    router as jurados_router
)

from app.routers.participantes import (
    router as participantes_router
)

from app.routers.publico import (
    router as publico_router
)

from app.routers.rubricas import (
    router as rubricas_router
)


app = FastAPI(
    title="Sistema 3MT - Backend",
    description=(
        "Microservicio backend para gestión de "
        "jurados, participantes, evaluaciones "
        "y votación pública."
    ),
    version="0.1.0"
)


app.include_router(
    participantes_router
)

app.include_router(
    jurados_router
)

app.include_router(
    evaluaciones_router
)

app.include_router(
    publico_router
)

app.include_router(
    rubricas_router
)


@app.get(
    "/health",
    tags=["Health"]
)
def health():

    return {
        "status": "ok",
        "service": "backend-sistema-jurados"
    }


@app.get(
    "/",
    tags=["Root"]
)
def root():

    return {
        "message": (
            "Sistema 3MT API funcionando correctamente."
        )
    }