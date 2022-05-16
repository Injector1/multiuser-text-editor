import os
import subprocess
from typing import List

from database import SessionLocal, engine
from database import models, schemas, repository
from connection_manager import ConnectionManager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from starlette.responses import FileResponse


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
    file_name = 'first.txt'
    file_content = "".join(open('./files/' + file_name, 'r', encoding='utf-8'))
    os.system(" ".join(['python', '../cui/editor.py', file_name, file_content]))
    return FileResponse('static/main.html')


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


@app.get('/files')
async def get_files():
    return FileResponse('./files/first.txt', media_type='application/octet-stream', filename='first.txt')
