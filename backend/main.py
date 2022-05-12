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
def get_files():
    return FileResponse('./files/first.txt', media_type='application/octet-stream', filename='first.txt')