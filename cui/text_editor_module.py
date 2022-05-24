import sys
import keyboard
import pyautogui
import curses
from uuid import uuid1
from time import time

from config import *
from ws import send_message


is_end = False
file_name = ""


def update() -> None:
	pyautogui.hotkey('enter')


def end_session() -> None:
	global is_end
	is_end = True
	curses.endwin()
	update()


def connect_to_editor(file: str) -> None:
	global file_name
	file_name = file
	keyboard.add_hotkey('f5', end_session)
	update()
	edit_file()


def edit_file() -> None:
	global is_end
	content = get_text_from_server()
	cui = curses.initscr()
	cui.addstr(0, 0, content)
	while not is_end:
		key = cui.getkey()
		if is_end:
			break
		content += key
		synchronize_data(cui, content)


def synchronize_data(cui, content: str) -> None:
	if int(time()) % 5 == 0:
		send_text_to_server(content)
		cui.addstr(0, 0, get_text_from_server())


def get_text_from_server() -> str:
	with open(directory + file_name, 'r', encoding='utf-8') as f:
		return "".join(f)


def send_text_to_server(message: str) -> None:
	client_id = str(uuid1())
	send_message(client_id, file_name, message)


if __name__ == '__main__':
	connect_to_editor(sys.argv[1])
