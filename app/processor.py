import os
import sys
import readline
import subprocess

from app.constants import Constants
from app.utils import valid_commands, parse_input

class Processor:
    def __init__(self):
        path = os.environ.get('PATH')
        self.paths = path.split(':') if path else []
        self.home = os.environ.get('HOME')
        self.enable_autocomplete()
    
    def start(self):
        sys.stdout.write("$ ")

        while True:
            input_str = input()
            command, args, stdout_file, stderr_file = parse_input(input_str)

            if command == Constants.EXIT:
                exit_code = int(args[0]) if args else 0
                sys.exit(exit_code)
            
            output, error = self.process(command, args)

            pairs = [
                (output, stdout_file),
                (error, stderr_file)
            ]

            for text, file in pairs:
                if file:
                    with open(file, 'a') as f:
                        if text: f.write(text + '\n')
                elif text:
                    print(text)

            sys.stdout.write("$ ")

    def process(self, command: str, args: list[str]) -> tuple[str | None, str | None]:
        match command:
            case Constants.ECHO:
                return ' '.join(args), None
            
            case Constants.TYPE:
                is_builtin = args[0] in valid_commands
                is_executable, exec_path = self.is_command_executable(args[0])
                
                if is_builtin:
                    return f'{args[0]} is a shell builtin', None
                elif is_executable:
                    return f'{args[0]} is {exec_path}', None
                else:
                    return None, f'{args[0]}: not found'

            case Constants.PWD:
                return os.getcwd(), None
            
            case Constants.CD:
                try:
                    os.chdir(self.home if args[0] == '~' else args[0])
                    return None, None
                except FileNotFoundError:
                    return None, f'cd: {args[0]}: No such file or directory'
            
            case _:
                is_executable, exec_path = self.is_command_executable(command)
                if is_executable:
                    exe_name = os.path.basename(exec_path)
                    exe_dir = os.path.dirname(exec_path)

                    result = subprocess.run(
                        [exe_name] + args, 
                        cwd=exe_dir,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    return result.stdout.rstrip(), result.stderr.rstrip()

                else:
                    return None, f'{command}: command not found'

    def is_command_executable(self, command: str):
        for path in self.paths:
            full_path = os.path.join(path, command)
            if os.access(full_path, os.X_OK):
                return True, full_path
        return False, None

    def complete_command(self, text: str, state: int):
        if not text:
            return None

        suggestions = [f'{cmd} ' for cmd in valid_commands if cmd.startswith(text)]

        for path in self.paths:
            if os.path.isdir(path):
                try:
                    suggestions += [f'{exe} ' for exe in os.listdir(path) if exe.startswith(text)]
                except PermissionError:
                    pass  # Ignore unreadable directories

        return suggestions[state] if state < len(suggestions) else None
    
    def enable_autocomplete(self):
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.complete_command)