from ..tool import Formatter, CommandMixin
from ..util import get_path


class Black(CommandMixin, Formatter):
    default_command = "black"

    def construct_command_args(self, files):
        args = self.get_command()

        line_length = get_path(self.config, "config.line-length")
        if line_length is not None:
            args.append("--line-length={:d}".format(line_length))

        for opt in [
            "py36",
            "pyi",
            "skip-string-normalization",
            "skip-numeric-underscore-normalization",
        ]:
            if get_path(self.config, ("config", opt), False):
                args.append("--" + opt)

        args.append("--")

        return args + files
