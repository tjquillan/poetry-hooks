from typing import Any

from cleo.events.console_command_event import ConsoleCommandEvent
from cleo.events.console_events import COMMAND, TERMINATE
from cleo.io.inputs.argv_input import ArgvInput
from cleo.io.inputs.string_input import StringInput
from cleo.io.io import IO
from poetry.console.application import Application
from poetry.console.commands.command import Command
from poetry.plugins import ApplicationPlugin

from poetry_hooks.commands.add import AddCommand
from poetry_hooks.commands.run import RunCommand


class PoetryHooks(ApplicationPlugin):
    def activate(self, application: Application) -> None:
        application.command_loader.register_factory("hook add", AddCommand.factory)
        application.command_loader.register_factory("hook run", RunCommand.factory)

        self._application = application

        if (event_dispatcher := application.event_dispatcher) is not None:
            event_dispatcher.add_listener(COMMAND, self.run_pre_hooks)
            event_dispatcher.add_listener(TERMINATE, self.run_post_hooks)

    def run_pre_hooks(self, event: ConsoleCommandEvent, *_: Any) -> None:
        command_name: str = event.command.name.replace(" ", "_")
        self._run_command(RunCommand(), event.io, f"pre{command_name}")

    def run_post_hooks(self, event: ConsoleCommandEvent, *_: Any) -> None:
        command_name: str = event.command.name.replace(" ", "_")
        self._run_command(RunCommand(), event.io, f"post{command_name}")

    def _run_command(self, command: Command, io: IO, args: str) -> None:
        command.set_application(self._application)
        command.set_poetry(self._application.poetry)
        input = StringInput(args)
        if " " in command.name:
            argv = [self._application.name, command.name] + input._tokens
            input = ArgvInput(argv)
        else:
            input = StringInput(command.name + " " + args)
        command.run(io.with_input(input))
