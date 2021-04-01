import typer
from lrphase import InputData
from pathlib import Path
#from utils import metadata


APP_NAME = "LRphase"
app = typer.Typer()#help="LRphase: Phase individual reads using haplotype information.")

@app.callback()
def callback(ctx: typer.Context):
    """
    LRphase: Phase individual reads using haplotype information.

    Manage users CLI app.

    Use it with the create command.

    A new user with the given NAME will be created.
    """
    typer.echo(f"About to execute command: {ctx.invoked_subcommand}")


@app.command()
def directory():
    app_dir = typer.get_app_dir(APP_NAME)
    config_path: Path = Path(app_dir) / "config.json"
    typer.echo(app_dir)
    typer.echo(config_path)
    if not config_path.is_file():
        typer.echo("Config file doesn't exist yet")

@app.command()
def config_file():
    app_dir = typer.get_app_dir(APP_NAME)
    app_dir_path = Path(app_dir)
    app_dir_path.mkdir(parents=True, exist_ok=True)
    config_path: Path = Path(app_dir) / "config.json"
    if not config_path.is_file():
        config_path.write_text('{"version": "1.0.0"}')
    config_file_str = str(config_path)
    typer.echo("Opening config directory" + config_file_str)
    typer.launch(config_file_str, locate=True)

def hello_world():
    """our first CLI with typer!
    """
    typer.echo("Opening blog post...")
    typer.launch(
        "https://pluralsight.com/tech-blog/python-cli-utilities-with-poetry-and-typer"
    )

@app.command()
def create(username: str):
    """
    Create a new user with USERNAME.
    """
    typer.echo(f"Creating user: {username}")
    
    #hello_world()
    

@app.command()
def delete(
    username: str,
    force: bool = typer.Option(
        ...,
        prompt="Are you sure you want to delete the user?",
        help="Force deletion without confirmation.",
    ),
):
    """
    
    Delete a user with USERNAME.

    If --force is not used, will ask for confirmation.
    """
    if force:
        typer.echo(f"Deleting user: {username}")
    else:
        typer.echo("Operation cancelled")


@app.command()
def delete_all(
    force: bool = typer.Option(
        ...,
        prompt="Are you sure you want to delete ALL users?",
        help="Force deletion without confirmation.",
    )
):
    
    """

    Delete ALL users in the database.

    If --force is not used, will ask for confirmation.
    """
    if force:
        typer.echo("Deleting all users")
    else:
        typer.echo("Operation cancelled")


@app.command()
def init():
    """
    Initialize the users database.
    """
    typer.echo("Initializing user database")

#print('9')


def run() -> None:
    """
    Run commands.
    """
    #typer.run(hello_world)
    #typer.echo('g')
    app()

#if __name__ == "__main__":
#    app()
#    typer.run(hello_world)
#    print('after')
