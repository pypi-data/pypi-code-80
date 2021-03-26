import pathlib

from dict_tools.data import NamespaceDict

if __name__ == "__main__":
    ctx = NamespaceDict({{cookiecutter}})
    root_directory = pathlib.Path.cwd()

    for dyne in ctx.dyne_list:
        if not root_directory.exists():
            root_directory.mkdir()
        if not (root_directory / ctx.clean_name).exists():
            (root_directory / ctx.clean_name).mkdir()
        if not (root_directory / ctx.clean_name / dyne).exists():
            (root_directory / ctx.clean_name / dyne).mkdir()
        if not (root_directory / ctx.clean_name / dyne / "contracts").exists():
            (root_directory / ctx.clean_name / dyne / "contracts").mkdir()
