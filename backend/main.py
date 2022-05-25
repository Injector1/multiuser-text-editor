from typing import List

from database import SessionLocal, engine
from database import models, schemas, repository
from connection_manager import ConnectionManager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from starlette.responses import FileResponse
from os import listdir
from os.path import isfile, join


def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


models.Base.metadata.create_all(bind=engine)
app = FastAPI()
db = get_db()
manager = ConnectionManager(db)


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
        print("Client left text editting")


@app.get('/files')
def get_files():
    return {'files': [f for f in listdir('./files') if isfile(join('./files', f))]}

