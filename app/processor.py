import os
import sys
import subprocess

from app.state import State
from app.constants import Constants
from app.utils import valid_commands, parse_input

class Processor:
    def __init__(self):
        self.state = State()
    
    def start(self):
        sys.stdout.write("$ ")

        while True:
            input_str = input()
            command, args = parse_input(input_str)

            if command == Constants.EXIT:
                break

            self.process(command, args)
            sys.stdout.write("$ ")

    def process(self, command: str, args: list):
        match command:
            case Constants.ECHO:
                print(' '.join(args))
            
            case Constants.TYPE:
                is_builtin = args[0] in valid_commands
                is_executable, exec_path = self.is_command_executable(args[0])
                
                if is_builtin:
                    print(f'{args[0]} is a shell builtin')
                elif is_executable:
                    print(f'{args[0]} is {exec_path}')
                else:
                    print(f'{args[0]}: not found')
            
            case _:
                is_executable, exec_path = self.is_command_executable(command)
                if is_executable:
                    exe_name = os.path.basename(exec_path)
                    exe_dir = os.path.dirname(exec_path)
                    subprocess.run([exe_name] + args, cwd=exe_dir)
                else:
                    print(f'{command}: command not found')

    def is_command_executable(self, command: str) -> bool:
        for path in self.state.paths:
            if os.access(os.path.join(path, command), os.X_OK):
                return True, os.path.join(path, command)
        return False, None