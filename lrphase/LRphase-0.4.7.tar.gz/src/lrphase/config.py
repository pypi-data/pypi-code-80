  
#from colab_cli.cli_new import cli_new
#from colab_cli.cli_pull import cli_pull
#from colab_cli.cli_open import cli_open
from shutil import copy
from pathlib import Path
import typer
import json
import glob
import os

#from colab_cli.cli_push import cli_push
from utils import GetMetadata
#from colab_cli.utilities.path_process import process_file_path


APP_NAME = "LRphase"
app_dir = typer.get_app_dir(APP_NAME)
app_dir = Path(app_dir)
config_path = app_dir / 'config.json'

config = typer.Typer()


@config.callback()
def callback():
    """
    Config file for LRphase
    """


@config.command()
def set_auth_user(user_no: str):
    """
      Set auth user, count start from zero
      """
    config_file = {'auth_user_id': user_no}
    print(config_file)
    print(config_path)
    with open(config_path, "w") as f:
        json.dump(config_file, f)


@config.command()
def set_config(file_path: Path = typer.Argument(
    ...,
    exists=True,
    file_okay=True,
    dir_okay=False,
    writable=False,
    readable=True,
    resolve_path=True,
)):
    """
      Set client_secrets.json for colab-cli
      """
    if file_path is None:
        typer.echo("No file")
        raise typer.Abort()
    if file_path.is_file():
        app_dir.mkdir(parents=True, exist_ok=True)
        copy(str(file_path), str(app_dir))
        typer.echo("Config File set Successfully")
    elif file_path.is_dir():
        typer.echo("is a directory")
    elif not file_path.exists():
        typer.echo("The file doesn't exist")


@config.command()
def list_nb():
    """
      list ipynb in current directory
      """
    for file in glob.glob("*.ipynb"):
        print(f"{file}")


@config.command()
def new_nb(file_path: Path = typer.Argument(
    ...,
    exists=False,
    file_okay=True,
    dir_okay=False,
    writable=False,
    readable=True,
    resolve_path=True,
)):
    """
    Create ipynb in colab
    Note: Useful cmd in new projects
    """
    if file_path is None:
        typer.echo("No file")
        raise typer.Abort()
    if file_path.is_file():
        # folder_struct_list, upload_file_name, file_path = process_file_path(file_path)
        # cli_new(folder_struct_list, upload_file_name, file_path)
        typer.echo("file already exist try : open-nb ")
        pass
    elif file_path.is_dir():
        typer.echo("is a directory")
    elif not file_path.exists():
        file_name = os.path.basename(file_path)
        colab_meta_data = GetMetadata.get_colab_metadata(file_name)
        with open(file_name, 'w') as fp:
            fp.write(json.dumps(colab_meta_data))
        folder_struct_list, upload_file_name, file_path = process_file_path(file_path)
        cli_new(folder_struct_list, upload_file_name, file_path)

def run():
    config()
