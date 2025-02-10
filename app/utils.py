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
    return command, args
