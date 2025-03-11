import os
import sys
import subprocess

from app.constants import Constants
from app.utils import valid_commands, parse_input

class Processor:
    def __init__(self):
        path = os.environ.get('PATH')
        self.paths = path.split(':') if path else []
        self.home = os.environ.get('HOME')
    
    def start(self):
        sys.stdout.write("$ ")

        while True:
            input_str = input()
            command, args, output_file = parse_input(input_str)

            if command == Constants.EXIT:
                exit_code = int(args[0]) if args else 0
                sys.exit(exit_code)

            output = self.process(command, args)

            if output and output_file:
                with open(output_file, 'a') as f:
                    f.write(output + '\n')
            elif output:
                print(output)

            sys.stdout.write("$ ")

    def process(self, command: str, args: list):
        match command:
            case Constants.ECHO:
                return ' '.join(args)
            
            case Constants.TYPE:
                is_builtin = args[0] in valid_commands
                is_executable, exec_path = self.is_command_executable(args[0])
                
                if is_builtin:
                    return f'{args[0]} is a shell builtin'
                elif is_executable:
                    return f'{args[0]} is {exec_path}'
                else:
                    return f'{args[0]}: not found'

            case Constants.PWD:
                return os.getcwd()
            
            case Constants.CD:
                try:
                    os.chdir(self.home if args[0] == '~' else args[0])
                    return
                except FileNotFoundError:
                    return f'cd: {args[0]}: No such file or directory'
            
            case _:
                is_executable, exec_path = self.is_command_executable(command)
                if is_executable:
                    exe_name = os.path.basename(exec_path)
                    exe_dir = os.path.dirname(exec_path)

                    result = subprocess.run(
                        [exe_name] + args, 
                        cwd=exe_dir,
                        stdout=subprocess.PIPE,
                        text=True
                    )
                    return result.stdout.rstrip()

                else:
                    return f'{command}: command not found'

    def is_command_executable(self, command: str):
        for path in self.paths:
            full_path = os.path.join(path, command)
            if os.access(full_path, os.X_OK):
                return True, full_path
        return False, None