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

        case Constants.TYPE:
            valid_constants = [
                getattr(Constants, attr)
                for attr in dir(Constants)
                if attr.isupper() and not callable(getattr(Constants, attr))
            ]
            is_builtin = args[0] in valid_constants
            print(f'{args[0]} is a shell builtin' if is_builtin else f'{args[0]}: not found')
        
        case _:
            print(f'{command}: command not found')

if __name__ == "__main__":
    main()
