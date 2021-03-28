import pathlib

import pop.hub
from dict_tools.data import NamespaceDict

if __name__ == "__main__":
    ctx = NamespaceDict({{cookiecutter}})
    root_directory = pathlib.Path.cwd()

    hub = pop.hub.Hub()
    hub.pop.sub.add(dyne_name="tool")

    for dyne in ctx.dyne_list:
        hub.tool.path.mkdir(root_directory / ctx.clean_name / dyne / "contracts")
