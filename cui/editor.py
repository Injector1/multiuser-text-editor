import os
import sys

from text_editor_module import edit_file_with_curses


dir = './multiuser-text-editor/backend/files/'


def write_new_content(new_content, file_name):
    file = open(dir + file_name, 'w', encoding='utf-8')
    file.write(new_content)
    file.close()


def edit_file(*args):
    text = edit_file_with_curses(args[0])
    os.system('cls')
    write_new_content(text, args[1])
    return


if __name__ == "__main__":
    content = " ".join(sys.argv[2:])
    edit_file(content, sys.argv[1])
