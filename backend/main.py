import uuid
from typing import Tuple, Dict

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from py3crdt.gset import GSet

app = FastAPI()

current_text = GSet(id=uuid.uuid4())

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Tuple[GSet, WebSocket]] = {}
        self.current_text: GSet = GSet(id=1)

    async def connect(self, websocket: WebSocket):
        websocket_id = str(uuid.uuid4())
        await websocket.accept()
        self.active_connections[websocket_id] = (GSet(id=websocket_id), websocket)
        return websocket_id

    def disconnect(self, websocket_id: str):
        del self.active_connections[websocket_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, user_websocket_id: str, message: str):
        text = GSet(id=uuid.uuid4())
        text.add(message)

        current_text.merge(text)
        print(current_text.display())
        # for websocket_id in self.active_connections:
        #     print(websocket_id)
        #     if user_websocket_id == websocket_id:
        #         print("AAAA", self.active_connections[websocket_id][0].display())
        #         user_message = self.active_connections[websocket_id][0].add(message)
        #         print(user_message)
        #     print(*self.current_text.display())
        #     await self.current_text.merge(self.active_connections[websocket_id][0])
        #     print(*self.current_text.display())
        #     await self.active_connections[websocket_id][1].send_text(*self.current_text.display())
        await self.active_connections[user_websocket_id][1].send_text(*current_text.display())


manager = ConnectionManager()


@app.get("/")
async def get():
    return FileResponse('main.html')


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket):
    websocket_id = await manager.connect(websocket)
    print(websocket_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(websocket_id, f"{data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket_id)
        await manager.broadcast(f"Client #{websocket_id} left the chat")
