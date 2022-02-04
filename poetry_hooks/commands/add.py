from poetry.console.commands.command import Command


class AddCommand(Command):
    @staticmethod
    def factory() -> "AddCommand":
        return AddCommand()

    name = "hook add"
