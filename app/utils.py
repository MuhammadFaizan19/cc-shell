import shlex
from typing import List, Tuple, Optional

from app.constants import Constants


valid_commands = [
    getattr(Constants, attr)
    for attr in dir(Constants)
    if attr.isupper() and not callable(getattr(Constants, attr))
]

def parse_input(input_str: str) -> Tuple[str, List[str], Optional[str], Optional[str]]:
    # -- Ideally this should be a custom parser
    tokens = shlex.split(input_str)
    if not tokens:
        return "", [], None, None

    command = tokens[0]
    args = []
    stdout_file = None
    stderr_file = None

    stdout_redirects = {">", "1>", ">>", "1>>"}
    stderr_redirects = {"2>", "2>>"}

    i = 1
    while i < len(tokens):
        if tokens[i] in stdout_redirects and i + 1 < len(tokens):
            stdout_file = tokens[i + 1]
            i += 2  # Skip the next token (the filename)
        elif tokens[i] in stderr_redirects and i + 1 < len(tokens):
            stderr_file = tokens[i + 1]
            i += 2 # Skip the next token (the filename)
        else:
            args.append(tokens[i])
            i += 1

    return command, args, stdout_file, stderr_file
