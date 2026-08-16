from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware,
)

from app.routers.admin_resultados import (
    router as admin_resultados_router,
)

from app.routers.admin_votacion import (
    router as admin_votacion_router,
)

from app.routers.evaluaciones import (
    router as evaluaciones_router,
)

from app.routers.jurados import (
    router as jurados_router,
)

from app.routers.participantes import (
    router as participantes_router,
)

from app.routers.publico import (
    router as publico_router,
)

from app.routers.rubricas import (
    router as rubricas_router,
)

from app.routers.websocket_resultados import (
    router as websocket_resultados_router,
)


app = FastAPI(
    title="Sistema 3MT - Backend",
    description=(
        "Microservicio backend para gestión "
        "de jurados, participantes, "
        "evaluaciones, resultados "
        "y votación pública."
    ),
    version="0.1.0",
)


origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]


app.add_middleware(
    CORSMiddleware,

    allow_origins=
        origins,

    allow_credentials=
        True,

    allow_methods=[
        "*"
    ],

    allow_headers=[
        "*"
    ],
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

app.include_router(
    admin_resultados_router
)

app.include_router(
    admin_votacion_router
)

app.include_router(
    websocket_resultados_router
)


@app.get(
    "/health",
    tags=["Health"],
)
def health():

    return {
        "status":
            "ok",

        "service":
            "backend-sistema-jurados",

        "realtime":
            True,
    }


@app.get(
    "/",
    tags=["Root"],
)
def root():

    return {
        "message":
            "Sistema 3MT API "
            "funcionando correctamente.",

        "websocket":
            "/ws/admin/resultados",
    }