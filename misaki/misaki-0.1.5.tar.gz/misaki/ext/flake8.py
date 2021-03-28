from ..tool import Linter, CommandMixin


class Flake8(CommandMixin, Linter):
    default_command = "flake8"

    def construct_command_args(self, files):
        args = self.get_command()
        args.append("--")
        args.extend(files)
        return args
