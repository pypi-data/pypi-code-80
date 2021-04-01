import typer
from LRphase import InputData

print('BEGINscript')
app = typer.Typer(help="LRphase: Phase individual reads using haplotype information.")
print('BEGIN')

@app.command()
def create(username: str):
    """
    Create a new user with USERNAME.
    """
    typer.echo(f"Creating user: {username}")
    

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
    print(5)
    Delete a user with USERNAME.

    If --force is not used, will ask for confirmation.
    """
    if force:
        print('6')
        typer.echo(f"Deleting user: {username}")
    else:
        print('7')
        typer.echo("Operation cancelled")


@app.command()
def delete_all(
    force: bool = typer.Option(
        ...,
        prompt="Are you sure you want to delete ALL users?",
        help="Force deletion without confirmation.",
    )
):
    print ('8')
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

print('9')

#if __name__ == "__main__":
#    print('DONE')
#    app()

print('p')