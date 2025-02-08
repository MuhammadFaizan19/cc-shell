from typing import List, Tuple

from app.constants import Constants


valid_commands = [
    getattr(Constants, attr)
    for attr in dir(Constants)
    if attr.isupper() and not callable(getattr(Constants, attr))
]

def parse_input(input_str: str) -> Tuple[str, List[str]]:
    items = input_str.split()
    command, args = items[0], items[1:]
    return command, args
