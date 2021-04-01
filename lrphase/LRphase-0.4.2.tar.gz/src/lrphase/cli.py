import typer
from lrphase import InputData

app = typer.Typer(help="LRphase: Phase individual reads using haplotype information.")

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
    hello_world()
    

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
