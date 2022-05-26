import curses
from time import sleep
import keyboard
import pyautogui
from WebSocket import WebSocket
from uuid import uuid1
from config import *
from multiprocessing import Process


class Editor:
	def __init__(self, file_name: str):
		self.file_name = file_name
		self.is_end = False
		self.text = self.get_text_from_server()
		self.ws = WebSocket(str(uuid1()), self.file_name)
		self.cui = None

	def run(self) -> None:
		p1 = Process(target=self.start_session)
		p2 = Process(target=self.update_local_text)

		self.setup_hotkeys()

		self.cui = curses.initscr()

		p1.start()
		p2.start()

		p1.join()
		p2.join()

	def start_session(self) -> None:
		self.cui.addstr(0, 0, self.text)
		while not self.is_end:
			self.cui.refresh()
			self.cui.clrtobot()

			key = self.cui.getkey()
			if key in '\b':
				continue
			if self.is_end:
				break
			self.add_text(key)
			self.update_server_text()

	def end_session(self) -> None:
		self.is_end = True
		self.ws.close_connection()
		curses.endwin()
		self.update()

	def add_text(self, key: str) -> None:
		y, x = self.cui.getyx()
		while len(list(self.text.split('\n'))) <= y:
			self.text += '\n'

		changed_line = list(self.text.split('\n')[y])
		changed_line.insert(x - 1, key)
		changed_line = ''.join(changed_line)

		if y > 0:
			self.text = '\n'.join(self.text.split('\n')[:y]) + \
			            '\n' + changed_line + \
			            '\n'.join(self.text.split('\n')[y + 1:])
		else:
			self.text = changed_line + '\n' + \
			            '\n'.join(self.text.split('\n')[1:])

		self.cui.addstr(0, 0, self.text)
		self.cui.refresh()
		self.move_mouse(y, x, 0.1)

	def move_mouse_up(self) -> None:
		y, x = self.cui.getyx()
		if y > 0:
			self.cui.move(y - 1, x)
		self.cui.refresh()

	def move_mouse_down(self) -> None:
		y, x = self.cui.getyx()
		if len(self.text.split('\n')) < y + 3:
			self.text += '\n'
		self.cui.move(y + 1, len(self.text.split('\n')[y + 1]))
		self.cui.refresh()

	def move_mouse_left(self) -> None:
		y, x = self.cui.getyx()
		if x > 0:
			self.cui.move(y, x - 1)
			self.cui.refresh()

	def move_mouse_right(self) -> None:
		y, x = self.cui.getyx()
		self.cui.move(y, x + 1)
		self.cui.refresh()

	def move_mouse(self, y: int, x: int, sec: float) -> None:
		sleep(sec)
		self.cui.move(y, x)
		self.cui.refresh()

	def delete_left_symbol(self) -> None:
		y, x = curses.getsyx()
		if x > 0:
			changed_text = list(self.text.split('\n')[y])
			changed_text[x - 1] = ''
			if y > 0:
				self.text = '\n'.join(self.text.split('\n')[:y]) + \
				            '\n' + ''.join(changed_text) + '\n'
				if len(self.text.split('\n')) > y:
					self.text += '\n'.join(self.text.split('\n')[y + 1:])
			else:
				self.text = ''.join(changed_text) + '\n' + \
				            '\n'.join(self.text.split('\n')[y + 1:])
			self.cui.addstr(0, 0, self.text)
			sleep(0.1)
			self.cui.refresh()
			self.move_mouse(y, x - 1, 0.15)

	def delete_right_symbol(self) -> None:
		y, x = self.cui.getyx()
		changed_text = list(self.text.split('\n')[y])
		changed_text[x] = ''
		if y > 0:
			self.text = '\n'.join(self.text.split('\n')[:y]) + \
			            '\n' + ''.join(changed_text) + '\n' + \
			            '\n'.join(self.text.split('\n')[y + 1:])
		else:
			self.text = ''.join(changed_text) + '\n' + \
			            '\n'.join(self.text.split('\n')[y + 1:])
		self.cui.refresh()
		self.cui.addstr(0, 0, self.text)
		self.cui.refresh()
		self.move_mouse(y, x, 0.15)

	def setup_hotkeys(self) -> None:
		hotkeys = {
			'esc': self.end_session,
			'up': self.move_mouse_up,
			'down': self.move_mouse_down,
			'left': self.move_mouse_left,
			'right': self.move_mouse_right,
			'backspace': self.delete_left_symbol,
			'delete': self.delete_right_symbol
		}

		for key, command in hotkeys.items():
			keyboard.add_hotkey(key, command)

	# def sync(self) -> None:
	# 	self.update_local_text(self.get_text_from_server())
	# 	self.update_server_text(self.text)

	def update_server_text(self) -> None:
		self.ws.send(self.text)
		sleep(1)

	def update_local_text(self, text: str) -> None:
		while not self.is_end:
			self.cui.addstr(0, 0, text)
			sleep(0.1)
			self.cui.refresh()
			sleep(1)

	def get_text_from_server(self) -> str:
		with open(directory + self.file_name, 'r', encoding='utf-8') as f:
			return "".join(f)

	@staticmethod
	def update() -> None:
		pyautogui.hotkey('enter')
