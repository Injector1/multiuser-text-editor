import curses
import curses.textpad


class Editor:
	def edit_file(self):
		return self.text_box.edit()

	def start(self, content):
		screen = curses.initscr()
		nw = curses.newwin(self.h, self.w, 0, 0)
		self.text_box = curses.textpad.Textbox(nw, insert_mode=True)
		nw.addstr(0, 0, content)
		screen.refresh()

	def close(self):
		self.stdscr.keypad(False)
		curses.echo()
		curses.nocbreak()
		curses.endwin()

	def __init__(self, height, width):
		self.h = height
		self.w = width

		self.stdscr = curses.initscr()
		curses.noecho()
		curses.cbreak()
		self.stdscr.keypad(True)
		self.stdscr.clear()
		self.stdscr.refresh()


def edit_file_with_curses(file_content):
	height = 30  # размеры окошка косноли не регулируются автоматом
	width = 120

	editor = Editor(height, width)

	editor.start(file_content)
	new_content = editor.edit_file()
	editor.close()

	return new_content
