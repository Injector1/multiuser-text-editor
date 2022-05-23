import uuid
from typing import Tuple, Dict, List
from os import listdir
from os.path import isfile, join
import json

from py3crdt.gset import GSet
from fastapi import WebSocket
from sqlalchemy.orm import Session

from database import repository


class ConnectionManager:
    def __init__(self, database_session: Session):
        self.base_dir = './files'
        self.available_files = [f for f in listdir(self.base_dir) if isfile(join(self.base_dir, f))]
        self.active_connections: Dict[str, List[(WebSocket, str)]] = dict.fromkeys(self.available_files, [])
        self.session = database_session

    async def connect(self, websocket: WebSocket, client_id: str, file_name: str):
        print(self.active_connections)
        if file_name in self.available_files:
            await websocket.accept()
            self.active_connections[file_name].append((websocket, client_id))
            await websocket.send_text(open(f'{self.base_dir}/{file_name}').read())
        return Exception('There is no such file')

    def disconnect(self, websocket: WebSocket):
        for key in self.active_connections:
            if websocket in self.active_connections[key]:
                del self.active_connections[key][self.active_connections[key].index(websocket)]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, file_name: str, data: str):
        serialized_json = json.loads(data)

        print(file_name, serialized_json)
        for active_file in self.active_connections:
            if active_file == file_name:
                with open(f'{self.base_dir}/{file_name}', 'w+') as file:
                    file_content = GSet(id=str(uuid.uuid1()))
                    user_additions = GSet(id=str(uuid.uuid1()))
                    file_content.add(file.read())
                    user_additions.add(serialized_json['value'])

                    file_content.merge(user_additions)
                    print(''.join(file_content.payload))
                    file.write(''.join(file_content.payload))
                    for connection in self.active_connections[active_file]:
                        await connection[0].send_text(''.join(file_content.payload))


