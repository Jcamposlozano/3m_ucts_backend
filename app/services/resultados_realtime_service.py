from sqlalchemy.orm import Session

from app.services.resultados_service import (
    obtener_resultados_admin
)

from app.websockets.resultados_manager import (
    manager_resultados
)


async def emitir_resultados_actualizados(
    db: Session
) -> None:

    resultados = obtener_resultados_admin(
        db=db
    )

    await manager_resultados.broadcast(
        {
            "tipo": "RESULTADOS_ACTUALIZADOS",
            "data": resultados
        }
    )