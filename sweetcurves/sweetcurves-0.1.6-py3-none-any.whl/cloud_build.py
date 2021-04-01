from pathlib import Path
from typing import Any, Dict

import yaml
from devtools import debug
from loguru import logger
from pydantic import AnyUrl
from toolz.curried import filter, map, pipe, unique

from sweetcurves.catelog import CloudBuildModel
from sweetcurves.helpers import write_result
from sweetcurves.paths import get_cloud_build


class CloudBuildConfig:
    def __init__(self, root: Path):
        self.build_file = get_cloud_build(root)
        current_yml = self.in_yaml
        self.bm = CloudBuildModel(**current_yml)
        # debug(self.bm)
        self._new_ctx = ""

    @property
    def in_yaml(self) -> Dict[str, Any]:
        return yaml.safe_load(self.build_file.read_text())

    @property
    def first(self):
        return self.bm.steps[0]

    @property
    def name(self) -> str:
        # steps = self.build_model.steps
        if not self.is_steps():
            return "Name not found"
        return self.bm.steps[0].get("name", "Name not found")

    @name.setter
    def name(self, _name: str):
        if not self.is_steps():
            self.bm.steps = [{"name": _name, "args": []}]
            return
        self.bm.steps[0].name = _name

    @property
    def destination(self) -> str:
        if not self.is_steps():
            return "Destination not found"
        candidates = self.kaniko_by_name("destination")
        if not candidates:
            return "Destination not found"

        return candidates[0]

    @destination.setter
    def destination(self, _name: str):

        dest = f"{_name}"

        build_set = ['build', '-t', dest]
        if not self.is_steps():
            self.bm.steps = [{"args": build_set}]
            return

        self.bm.steps[0].args = list(unique(build_set + self.bm.steps[0].args))
        self.bm.images = [dest]

    @property
    def context(self) -> str:
        return Path("." if not self._new_ctx else self._new_ctx)

    @context.setter
    def context(self, _location: Path):
        self._new_ctx = _location

    @property
    def dockerfile(self) -> str:
        return str(self.context / "Dockerfile")

    def kaniko_by_name(self, name: str, eq: bool = True):
        """
        Find the kiko arguments that have the given name.

        

        Args:
            name (str): The name of the kaniko argument.
            eq (bool, optional): Filters everything that starts witht that name if true. Defaults to True.

        Returns:
            List[str]: A list of args that either are or are not inside of the first steps list.
        """
        return pipe(self.first.args,
                    filter(lambda x: x.startswith(f"--{name}") == eq), list)

    def is_steps(self) -> bool:
        return len(self.bm.steps) > 0

    def set_env(self, envs: Dict[str, str]):

        curr_array = self.bm.options.env
        self.bm.options.env = curr_array + [
            f"{name}={value}" for name, value in envs.items()
        ]

        return self.bm.dict()

    def set_args(self, args: Dict[str, str]):
        args = [f"--{name}={str(value)}" for name, value in args.items()]
        if not self.is_steps():
            self.bm.steps = [{"args": args}]
            return self.bm.dict()

        self.bm.steps[0].args += args
        self.bm.steps[0].args = pipe(self.bm.steps[0].args, unique, list)
        return self.bm.dict()

    def set_build_args(self, build_args: Dict[str, str]):
        build_args = [
            f"--build-arg={name}={str(value)}"
            for name, value in build_args.items()
        ]

        if not self.is_steps():
            self.bm.steps = [{"args": build_args}]
            return self.bm.dict()

        self.bm.steps[0].args += build_args
        return self.bm.dict()

    def to_dict(self) -> Dict[str, str]:
        return self.bm.dict()
