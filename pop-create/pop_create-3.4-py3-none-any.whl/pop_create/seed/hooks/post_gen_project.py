import pathlib

from dict_tools.data import NamespaceDict

if __name__ == "__main__":
    ctx = NamespaceDict({{cookiecutter}})
    root_directory = pathlib.Path.cwd()

    if ctx.vertical:
        script = root_directory / ctx.clean_name / "scripts.py"
        try:
            script.unlink()
        except FileNotFoundError:
            ...

        run = root_directory / "run.py"
        try:
            run.unlink()
        except FileNotFoundError:
            ...

        init = root_directory / ctx.clean_name / ctx.clean_name / "init.py"
        try:
            init.unlink()
        except FileNotFoundError:
            ...

        try:
            non_vertical_dyne = root_directory / ctx.clean_name / ctx.clean_name
            non_vertical_dyne.rmdir()
        except:
            ...
