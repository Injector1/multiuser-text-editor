import os
#import curses


directory = './Files/'
files = os.listdir(directory)


def print_help_message(*args):
    print('Available commands:\n'
          '/exit - to terminate program\n'
          '/edit "file.txt" - to edit file.txt\n'
          '/files - to get file names from folder\n'
          '/help - get help message\n')


def clear_screen(*args):
    os.system("cls")


def open_file(*args):
    file_name = args[0]
    try:
        f = open(directory + file_name, 'r', encoding='utf-8').readlines()
        text = input("\n".join(f))
    except:
        print(f'Unable to read file "{file_name}"')


def print_files(*args):
    for file in files:
        print('*', file)


def main():
    clear_screen()
    print_help_message()
    while True:
        input_lines = input('\n/').split()
        clear_screen()
        command = input_lines[0]
        if command in commands.keys():
            content = "" if len(input_lines) == 1 else input_lines[1]
            commands[command](content)
        else:
            print_help_message()


commands = {
    "exit": exit,
    "edit": open_file,
    "files": print_files,
    "help": print_help_message
    }

if __name__ == "__main__":
    main()
