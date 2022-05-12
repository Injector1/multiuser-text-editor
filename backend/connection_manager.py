import uuid
from typing import Tuple, Dict

from py3crdt.gset import GSet
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Tuple[GSet, WebSocket]] = {}
        self.current_text: GSet = GSet(id=1)

    async def connect(self, websocket: WebSocket):
        websocket_id = str(uuid.uuid1())
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

        self.current_text.merge(text)
        print(self.current_text.display())
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
        await self.active_connections[user_websocket_id][1].send_text(*self.current_text.display())

