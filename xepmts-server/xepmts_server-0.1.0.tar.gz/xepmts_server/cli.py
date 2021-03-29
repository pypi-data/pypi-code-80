"""Console script for xepmts_server."""
import sys

import click
from flask.cli import with_appcontext
from flask.cli import FlaskGroup
from werkzeug.serving import run_simple
from xepmts_server import run_simple
import subprocess
import os
import pathlib

SOURCE_DIR = pathlib.Path(__file__).parent.parent


@click.group()
def main():
    """Console script for xepmts_server."""
    click.echo("Replace this message by putting your code into "
               "xepmts_server.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0

@main.command()
def serve():
    subprocess.call("python scripts/serve.py", shell=True)
    

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
