import shlex
from typing import List, Tuple

from app.constants import Constants


valid_commands = [
    getattr(Constants, attr)
    for attr in dir(Constants)
    if attr.isupper() and not callable(getattr(Constants, attr))
]

def parse_input(input_str: str) -> Tuple[str, List[str]]:
    # -- Ideally this should be a custom parser
    tokens = shlex.split(input_str)
    command = tokens[0] if tokens else ""
    args = tokens[1:] if len(tokens) > 1 else []
    output_file = None
    
    redirects = [">", "1>", '>>']

    for rd in redirects:
        if rd in args:
            idx = args.index(rd)
            output_file = args[idx + 1]
            args = args[:idx]
            break

    return command, args, output_file
