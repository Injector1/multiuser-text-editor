import websockets
import uuid
import asyncio
import json


def get_message() -> str:
	text = input(': ')
	message = json.dumps({'type': 'insert', 'value': text})
	return message


async def send_messages(client_id: str, file_name: str) -> None:
	async with websockets.connect(f"ws://localhost:8000/ws/{client_id}&{file_name}") as ws:
		while True:
			await ws.send(get_message())


def connect(client_id: str, file_name: str) -> None:
	asyncio.run(send_messages(client_id, file_name))


if __name__ == "__main__":
	connect(client_id=str(uuid.uuid1()), file_name="first.txt")
