import sys


def main():
    sys.stdout.write("$ ")

    while True:
        command = input()

        if command.startswith('exit'):
            break

        execute_command(command)

        sys.stdout.write("$ ")

def execute_command(command):
    print(f'{command}: command not found')

if __name__ == "__main__":
    main()
