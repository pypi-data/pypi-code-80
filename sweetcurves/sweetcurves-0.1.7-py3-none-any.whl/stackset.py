from pathlib import Path

import yaml
from devtools import debug
from loguru import logger

from sweetcurves.catelog import StackModel
from sweetcurves.paths import get_docker_file, get_stack_settings


class StackDockerContext:
    def __init__(self, root: Path):
        self.docker = get_docker_file(root)
        self.stack = get_stack_settings(root)
        self.stack_model: StackModel = StackModel(
            **yaml.safe_load(self.stack.read_text()))

        # We're going to be setting these
        self.ctx = self.docker.parent
        self.doc_name = self.docker.name


if __name__ == '__main__':
    root_dir = Path(__file__).parent.parent / "tests" / "shrinkwrap"
    StackDockerContext(root_dir)
