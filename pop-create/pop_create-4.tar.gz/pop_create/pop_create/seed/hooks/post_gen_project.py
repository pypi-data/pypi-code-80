import pathlib

import pop.hub
from dict_tools.data import NamespaceDict

if __name__ == "__main__":
    ctx = NamespaceDict({{cookiecutter}})
    root_directory = pathlib.Path.cwd()
    hub = pop.hub.Hub()
    hub.pop.sub.add(dyne_name="tool")

    if ctx.vertical:
        script = root_directory / ctx.clean_name / "scripts.py"
        hub.tool.path.delete(script)

        run = root_directory / "run.py"
        hub.tool.path.delete(run)

        non_vertical_dyne = root_directory / ctx.clean_name / ctx.clean_name
        hub.tool.path.rmtree(non_vertical_dyne)
