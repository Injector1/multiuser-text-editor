import websockets
import uuid
import asyncio
import json


async def connect(client_id: str, file_name: str, message: str) -> None:
	async with websockets.connect(f"ws://localhost:8000/ws/{client_id}&{file_name}") as ws:
			await ws.send(json.dumps({'type': 'insert', 'value': message}))


def send_message(client_id: str, file_name: str, message: str) -> None:
	asyncio.run(connect(client_id, file_name, message))


if __name__ == "__main__":
	send_message(client_id=str(uuid.uuid1()), file_name="first.txt", message="231")
