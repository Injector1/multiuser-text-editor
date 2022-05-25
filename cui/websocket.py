import json
import websocket
from config import host


class WebSocket:
	def __init__(self, client_id: str, file_name: str):
		self.id = client_id
		self.file = file_name
		self.ws = websocket.WebSocket()
		self.ws.connect(f'{host}{client_id}&{file_name}')

	def send_message(self, message: str):
		self.ws.send(json.dumps(
			{'type': 'insert',
			 'value': message}
		))

	def close_connection(self):
		self.ws.close()
