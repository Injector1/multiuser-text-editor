from typing import List

from connection_manager import ConnectionManager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from starlette.responses import FileResponse
from os import listdir
from os.path import isfile, join


app = FastAPI()
manager = ConnectionManager()


@app.get("/")
async def get():
    return FileResponse('static/main.html')


@app.websocket("/ws/{client_id}&{file_name}")
async def websocket_endpoint(websocket: WebSocket, client_id: str, file_name: str):
    response = await manager.connect(websocket, client_id, file_name)
    print(response)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(file_name, data)
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)
        print("Client left text editing")


@app.get('/files')
def get_files():
    return {'files': [f for f in listdir('./files') if isfile(join('./files', f))]}

