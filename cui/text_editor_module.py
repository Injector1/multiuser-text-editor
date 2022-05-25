import sys
from Editor import Editor


def edit_file(file: str):
	Editor(file)


if __name__ == '__main__':
	edit_file(sys.argv[1])
