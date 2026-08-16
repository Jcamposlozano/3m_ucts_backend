from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect
)

from app.websockets.resultados_manager import (
    manager_resultados
)


router = APIRouter(
    tags=["WebSocket Resultados"]
)


@router.websocket(
    "/ws/admin/resultados"
)
async def websocket_resultados(
    websocket: WebSocket
):

    await manager_resultados.connect(
        websocket
    )

    try:

        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:

        manager_resultados.disconnect(
            websocket
        )

    except Exception:

        manager_resultados.disconnect(
            websocket
        )