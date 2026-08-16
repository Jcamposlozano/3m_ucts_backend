from fastapi import WebSocket


class ResultadosConnectionManager:

    def __init__(self) -> None:

        self.active_connections: list[
            WebSocket
        ] = []


    # =====================================================
    # CONECTAR CLIENTE
    # =====================================================

    async def connect(
        self,
        websocket: WebSocket,
    ) -> None:

        await websocket.accept()

        self.active_connections.append(
            websocket
        )

        print(
            "WebSocket conectado. "
            f"Conexiones activas: "
            f"{len(self.active_connections)}"
        )


    # =====================================================
    # DESCONECTAR CLIENTE
    # =====================================================

    def disconnect(
        self,
        websocket: WebSocket,
    ) -> None:

        if websocket in self.active_connections:

            self.active_connections.remove(
                websocket
            )

        print(
            "WebSocket desconectado. "
            f"Conexiones activas: "
            f"{len(self.active_connections)}"
        )


    # =====================================================
    # BROADCAST
    # =====================================================

    async def broadcast(
        self,
        message: dict,
    ) -> None:

        conexiones_muertas: list[
            WebSocket
        ] = []


        for connection in (
            self.active_connections
        ):

            try:

                await connection.send_json(
                    message
                )

            except Exception as exc:

                print(
                    "Error enviando mensaje "
                    "WebSocket:",
                    exc,
                )

                conexiones_muertas.append(
                    connection
                )


        # ---------------------------------------------
        # ELIMINAR CONEXIONES QUE YA NO RESPONDEN
        # ---------------------------------------------

        for connection in conexiones_muertas:

            self.disconnect(
                connection
            )


manager_resultados = (
    ResultadosConnectionManager()
)