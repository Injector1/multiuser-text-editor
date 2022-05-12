from typing import List

from database import SessionLocal, engine
from database import models, schemas, repository
from connection_manager import ConnectionManager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
manager = ConnectionManager()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return repository.get_users(db, skip=skip, limit=limit)
