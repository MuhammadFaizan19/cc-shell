import sys

from app.constants import Constants

def main():
    sys.stdout.write("$ ")

    while True:
        user_input = input()

        if user_input.startswith(Constants.EXIT):
            break

        execute_command(user_input)

        sys.stdout.write("$ ")

def execute_command(command: str):
    items = command.split()
    command, args = items[0], items[1:]

    match command:
        case Constants.ECHO:
            print(' '.join(args))
        
        case _:
            print(f'{command}: command not found')

if __name__ == "__main__":
    main()
