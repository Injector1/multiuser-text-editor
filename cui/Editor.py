from WebSocket import WebSocket
from config import *

import curses
from uuid import uuid1
from pynput.keyboard import Key, Listener


class Editor:
	def __init__(self, file_name: str):
		self.file_name = file_name
		self.is_end = False
		self.text = self.get_text_from_server()
		self.ws = WebSocket(str(uuid1()), self.file_name)
		self.cui = None

	def run(self) -> None:
		self.cui = curses.initscr()
		self.start_session()

	def on_press(self, key: Key):
		self.update_local_text()
		if key == Key.esc:
			self.end_session()
			return False
		if key == Key.backspace:
			self.delete_left_symbol()
			self.update_server_text()
		elif key == Key.delete:
			self.delete_right_symbol()
			self.update_server_text()
		elif key == Key.up:
			self.move_mouse_up()
			self.update_server_text()
		elif key == Key.down:
			self.move_mouse_down()
		elif key == Key.left:
			self.move_mouse_left()
		elif key == Key.right:
			self.move_mouse_right()
		elif key == Key.space:
			self.add_text(' ')
			self.update_server_text()
		elif key == Key.enter:
			self.add_text('\n')
			self.update_server_text()
		elif "'" in str(key):
			self.add_text(str(key)[1])
			self.update_server_text()

	def start_session(self) -> None:
		self.cui.addstr(0, 0, self.text)
		with Listener(on_press=self.on_press) as l:
			self.cui.refresh()
			self.cui.clrtobot()
			l.join()

	def end_session(self) -> None:
		self.is_end = True
		self.ws.close_connection()
		curses.endwin()

	def build_text(self, changed_line: str, index: int) -> str:
		s = ""
		t = self.text.split('\n')
		for i in range(len(t)):
			if i == index:
				s += changed_line
			else:
				s += t[i]
			if i + 1 != len(t):
				s += '\n'
			else:
				s += ''
		return s

	def add_text(self, key: str) -> None:
		y, x = self.cui.getyx()
		while len(list(self.text.split('\n'))) <= y:
			self.text += '\n'
		changed_line = list(self.text.split('\n')[y])
		changed_line.insert(x, key)

		if y > 0:
			self.text = self.build_text(''.join(changed_line), y)
		else:
			self.text = ''.join(changed_line) + '\n' + \
			            '\n'.join(self.text.split('\n')[1:])

		self.cui.addstr(0, 0, self.text)
		self.cui.refresh()
		if key == '\n':
			self.move_mouse(y + 1, 0)
		else:
			self.move_mouse(y, x + 1)

	def delete_left_symbol(self) -> None:
		y, x = curses.getsyx()
		if x > 0:
			changed_text = list(self.text.split('\n')[y])
			changed_text[x - 1] = ''
			if y > 0:
				self.text = self.build_text(''.join(changed_text), y)
			else:
				self.text = ''.join(changed_text) + '\n' + \
				            '\n'.join(self.text.split('\n')[y + 1:])
			self.cui.addstr(0, 0, self.text)
			self.cui.refresh()
			self.move_mouse(y, x - 1)

	def delete_right_symbol(self) -> None:
		y, x = self.cui.getyx()
		changed_text = list(self.text.split('\n')[y])
		changed_text[x] = ''
		if y > 0:
			self.text = self.build_text(''.join(changed_text), y)
		else:
			self.text = ''.join(changed_text) + '\n' + \
			            '\n'.join(self.text.split('\n')[y + 1:])
		self.cui.addstr(0, 0, self.text)
		self.cui.refresh()
		self.move_mouse(y, x)

	def move_mouse_up(self) -> None:
		y, x = self.cui.getyx()
		if y > 0:
			self.move_mouse(y - 1, len(self.text.split('\n')[y - 1]))

	def move_mouse_down(self) -> None:
		y, x = self.cui.getyx()
		if len(self.text.split('\n')) < y + 2:
			self.add_text('\n')
		self.move_mouse(y + 1, len(self.text.split('\n')[y + 1]))

	def move_mouse_left(self) -> None:
		y, x = self.cui.getyx()
		if x > 0:
			self.move_mouse(y, x - 1)

	def move_mouse_right(self) -> None:
		y, x = self.cui.getyx()
		self.move_mouse(y, x + 1)

	def move_mouse(self, y: int, x: int) -> None:
		self.cui.move(y, x)
		self.cui.refresh()

	def update_local_text(self) -> None:
		self.text = self.get_text_from_server()
		self.cui.addstr(0, 0, self.text)
		self.cui.refresh()

	def get_text_from_server(self) -> str:
		with open(directory + self.file_name, 'r', encoding='utf-8') as f:
			return "".join(f)

	def update_server_text(self) -> None:
		self.ws.send(self.text)
