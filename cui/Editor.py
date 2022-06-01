from WebSocket import WebSocket
from config import *

import curses
from uuid import uuid1
from pynput.keyboard import Key, Listener


class Editor:
	def __init__(self, file_name: str):
		self.file_name = file_name
		self.is_end = False
		self.text = "".join(open(directory + self.file_name, 'r', encoding='utf-8'))
		self.ws = WebSocket(str(uuid1()), self.file_name)
		self.cui = None

	def run(self) -> None:
		self.cui = curses.initscr()
		self.start_session()

	def on_press(self, key: Key):
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

	def add_text(self, key: str) -> None:
		y, x = self.cui.getyx()
		while len(list(self.text.split('\n'))) <= y:
			self.text += '\n'

		changed_line = list(self.text.split('\n')[y])
		changed_line.insert(x, key)
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

	def move_mouse_up(self) -> None:
		y, x = self.cui.getyx()
		if y > 0:
			self.move_mouse(y - 1, len(self.text.split('\n')[y - 1]))

	def move_mouse_down(self) -> None:
		y, x = self.cui.getyx()
		if len(self.text.split('\n')) < y + 3:
			self.text += '\n'
		self.cui.move(y + 1, len(self.text.split('\n')[y + 1]))
		self.cui.refresh()

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
			self.cui.refresh()
			self.move_mouse(y, x - 1)

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
		self.move_mouse(y, x)

	def update_server_text(self) -> None:
		self.ws.send(self.text)
