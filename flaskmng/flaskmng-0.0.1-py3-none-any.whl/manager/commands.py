import click
from ..globals import MultiCommand

@click.group(cls=MultiCommand)
def manager():
    pass

@manager.command("startproject")
def startproject_command():
    print("STARTING PROJECT")