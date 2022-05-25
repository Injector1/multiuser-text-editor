import curses
import os
from time import sleep
import keyboard
import pyautogui

is_end = False
cui: type(curses.initscr())
text: str


def run_editor(content: str) -> str:
	global cui, text
	text = content
	cui = curses.initscr()

	cui.addstr(0, 0, text)
	while not is_end:
		cui.refresh()
		cui.clrtobot()
		key = cui.getkey()
		if is_end:
			break
		add_text(key)

	return text


def end_session() -> None:
	global is_end
	is_end = True
	curses.endwin()
	update()


def add_text(key: str):
	global cui, text
	y, x = cui.getyx()
	while len(list(text.split('\n'))) <= y:
		text += '\n'

	changed_line = list(text.split('\n')[y])
	changed_line.insert(x - 1, key)
	changed_line = ''.join(changed_line)

	if y > 0:
		text = '\n'.join(text.split('\n')[:y]) + \
		       '\n' + changed_line + \
		       '\n'.join(text.split('\n')[y + 1:])
	else:
		text = changed_line + '\n' + \
		       '\n'.join(text.split('\n')[1:])

	cui.addstr(0, 0, text)
	cui.refresh()
	move_mouse(y, x, 0.05)


def move_mouse_up():
	global cui
	y, x = cui.getyx()
	if y > 0:
		cui.move(y - 1, x)
	cui.refresh()


def move_mouse_down():
	global cui, text
	y, x = cui.getyx()
	if len(text.split('\n')) < y + 3:
		text += '\n'
	cui.move(y + 1, len(text.split('\n')[y + 1]))
	cui.refresh()


def move_mouse_left():
	global cui, text
	y, x = cui.getyx()
	if x > 0:
		cui.move(y, x - 1)
	cui.refresh()


def move_mouse_right():
	global cui, text
	y, x = cui.getyx()
	cui.move(y, x + 1)
	cui.refresh()


def move_mouse(y: int, x: int, sec: float):
	global cui
	sleep(sec)
	cui.move(y, x)
	cui.refresh()


def delete_left_symbol():
	global cui, text
	y, x = curses.getsyx()

	if x > 0:
		changed_text = list(text.split('\n')[y])
		changed_text[x - 1] = ''
		if y > 0:
			text = '\n'.join(text.split('\n')[:y]) + \
			       '\n' + ''.join(changed_text) + '\n'
			if len(text.split('\n')) > y:
				text += '\n'.join(text.split('\n')[y + 1:])
		else:
			text = ''.join(changed_text) + '\n' + \
			       '\n'.join(text.split('\n')[y + 1:])
		cui.addstr(0, 0, text)
		sleep(0.1)
		cui.refresh()
		move_mouse(y, x - 1, 0.15)


def delete_right_symbol():
	global cui, text
	y, x = cui.getyx()
	changed_text = list(text.split('\n')[y])
	changed_text[x] = ''
	if y > 0:
		text = '\n'.join(text.split('\n')[:y]) + \
		       '\n' + ''.join(changed_text) + '\n' + \
		       '\n'.join(text.split('\n')[y + 1:])
	else:
		text = ''.join(changed_text) + '\n' + \
		       '\n'.join(text.split('\n')[y + 1:])
	cui.refresh()
	cui.addstr(0, 0, text)
	cui.refresh()


def update() -> None:
	pyautogui.hotkey('enter')


def setup_hotkeys():
	for key, command in hotkeys.items():
		keyboard.add_hotkey(key, command)


hotkeys = {
	'f5': end_session,
	'up': move_mouse_up,
	'down': move_mouse_down,
	'left': move_mouse_left,
	'right': move_mouse_right,
	'backspace': delete_left_symbol,
	'delete': delete_right_symbol
}

if __name__ == '__main__':
	setup_hotkeys()
	update()

	new_text = run_editor('negr\nbebra')
	os.system('cls')
	print('-' * 10)
	print(new_text)
	print('-' * 10)
