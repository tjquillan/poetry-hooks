from poetry.console.commands.command import Command


def run(command: str, parent: Command) -> None:
    parent.call("run", f"run {command}")
