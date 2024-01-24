from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_json(self, value, websocket: WebSocket):
        await websocket.send_json(value)

    async def disconnect(self, websocket: WebSocket):
        await websocket.close()
        self.active_connections.remove(websocket)
