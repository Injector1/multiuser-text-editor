import uuid
from typing import Dict, List
from os import listdir
from os.path import isfile, join
import json

from py3crdt.gset import GSet
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.base_dir = './files'
        self.available_files = [f for f in listdir(self.base_dir) if isfile(join(self.base_dir, f))]
        self.active_connections: Dict[str, List[(WebSocket, str)]] = dict.fromkeys(self.available_files, [])

    async def connect(self, websocket: WebSocket, client_id: str, file_name: str):
        if file_name in self.available_files:
            response = {'content': open(f'{self.base_dir}/{file_name}').read(), 'cursor': {'x': 0, 'y': 0}}
            await websocket.accept()
            self.active_connections[file_name].append((websocket, client_id))
            await websocket.send_text(json.dumps(response))
        return Exception('There is no such file')

    def disconnect(self, websocket: WebSocket, client_id: str):
        for key in self.active_connections:
            if (websocket, client_id) in self.active_connections[key]:
                print(self.active_connections[key][self.active_connections[key].index((websocket, client_id))])
                del self.active_connections[key][self.active_connections[key].index((websocket, client_id))]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, file_name: str, data: str):
        serialized_json = json.loads(data)
        user_cursor = serialized_json['cursor']
        response = {'content': '', 'cursor': {'x': user_cursor['x'], 'y': user_cursor['y']}}

        for active_file in self.active_connections:
            if active_file == file_name:
                with open(f'{self.base_dir}/{file_name}', 'w+') as file:
                    file_content = GSet(id=str(uuid.uuid1()))
                    user_additions = GSet(id=str(uuid.uuid1()))
                    file_content.add(file.read())
                    user_additions.add(serialized_json['value'])

                    file_content.merge(user_additions)
                    response['content'] = ''.join(file_content.payload)

                    file.write(response['content'])
                    for connection in self.active_connections[active_file]:
                        await connection[0].send_text(json.dumps(response))


