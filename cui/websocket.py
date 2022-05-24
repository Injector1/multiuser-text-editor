import json

import websocket


class WebSocket:
	def __init__(self, client_id: str, file_name: str):
		self.id = client_id
		self.file = file_name
		self.ws = websocket.WebSocket()
		self.ws.connect(f"ws://localhost:8000/ws/{self.id}&{self.file}")

	def send_message(self, message: str):
		self.ws.send(json.dumps(message))
