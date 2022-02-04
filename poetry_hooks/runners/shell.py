from subprocess import call
from typing import Any


def run(command: str, *_: Any) -> None:
    call(command.split(" "))
