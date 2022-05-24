from WebSocket import WebSocket
from uuid import uuid1


ws = WebSocket(str(uuid1()), "first.txt")

ws.send_message(message={'type': 'insert', 'value': 'BEBRAhi'})
a = input()
ws.send_message(message={'type': 'insert', 'value': 'hibebra'})
a = input()
ws.send_message(message={'type': 'insert', 'value': 'hibebra\nNIGGER'})
a = input()
