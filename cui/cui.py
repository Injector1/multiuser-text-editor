import os
from text_editor_module import edit_file_with_curses
from config import *


def create_file(filename):
    new_file = open(directory + filename, "w+")
    new_file.close()
    files.append(filename)
    edit_file(filename)


def print_help_message(*args):
    clear_screen()
    print(all_commands)


def clear_screen(*args):
    os.system("cls")


def open_file(*args):
    file_name = args[0]
    if file_name in files:
        edit_file(file_name)
    else:
        confirmation = input(creating_file)
        if confirmation.lower() == 'y':
            create_file(file_name)
        else:
            print_help_message()


def write_new_content(file_name, new_content):
    file = open(directory + file_name, 'w', encoding='utf-8')
    file.write(new_content)
    file.close()


def edit_file(*args):
    file_name = args[0]
    file_content = open(directory + file_name, 'r', encoding='utf-8')
    text = edit_file_with_curses("".join(file_content))
    clear_screen()
    try:
        write_new_content(file_name, text)
        print(f'File {file_name} was successfully edited!\n'
              'Enter any command to return to the menu')
    except:
        print('Some Errors while editing file')
        print(print_help_message())


def print_files(*args):
    clear_screen()
    for file in files:
        print('*', file)


files = os.listdir(directory)

commands = {
    "exit": exit,
    "edit": open_file,
    "files": print_files,
    "help": print_help_message
    }

if __name__ == "__main__":
    print_help_message()
    while True:
        input_lines = input('\n/').split()
        command = input_lines[0]
        if command in commands.keys():
            content = "" if len(input_lines) == 1 else input_lines[1]
            commands[command](content)
        else:
            print_help_message()
