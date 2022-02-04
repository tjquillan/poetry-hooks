from importlib import import_module
from typing import Optional

from cleo.helpers import argument
from poetry.console.commands.command import Command


class RunCommand(Command):
    @staticmethod
    def factory() -> "RunCommand":
        return RunCommand()

    name = "hook run"
    arguments = [argument("hook", "The hook to be run")]

    def handle(self) -> int:
        hook_id: str = self.argument("hook")

        config_parent = self.poetry.file.read()["tool"]
        if (
            "poetry-hooks" in config_parent
            and (config := config_parent["poetry-hooks"]).is_table()
            and hook_id in config
        ):
            hook = config[hook_id]

            self.line(f"<info>Running hook: {hook_id}</info>")
            if isinstance(hook, list):
                for item in hook:
                    self._run_hook(item)
            else:
                self._run_hook(hook)
        return 0

    def _run_hook(self, hook: str | dict[str, str]) -> int:
        type = "shell"
        command: Optional[str] = None
        if isinstance(hook, dict):
            type = hook["type"]
            command = hook["command"]
        else:
            command = hook

        self.line(f"<info>Running command: '{command}' with {type}</info>")

        try:
            module = import_module(f"poetry_hooks.runners.{type}")
        except ModuleNotFoundError:
            self.line(f"<error>Bad runner type: {type}</error>")
            return 1
        else:
            return module.run(command, self)
