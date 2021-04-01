import base64
import os
from enum import Enum
from pathlib import Path

import pyperclip
import typer
from loguru import logger
from sh import ErrorReturnCode, ErrorReturnCode_2

from sweetcurves import shells
from sweetcurves.complete import update_builds
from sweetcurves.paths import (get_build_folder, get_cloud_build,
                               get_docker_file)


class ConvertTo(str, Enum):
    BASE = "base"
    JSON = "json"


def current_path_files():
    return list(map(lambda x: x.name, Path().cwd().glob("**/*")))


app = typer.Typer()


@app.callback()
def main():
    """
        # Sweets
        
        CLI tool to help automate parts of the build process.
    """


@app.command()
def pathfind():
    """
        Find the build directory from in the working directory.
    """
    working_directory: Path = Path.cwd()
    relative_build_folder = None
    try:
        build_folder = get_docker_file(working_directory).parent
        relative_build_folder = build_folder.relative_to(working_directory)

    except Exception as e:
        typer.secho(
            "A build folder wasn't found. Going to use the current working directory."
        )

    typer.echo(
        f"gcloud builds submit {relative_build_folder} --config cloudbuild.yml --substitutions=GCP_KEY=$GCR_MAX"
    )


@app.command()
def transfers(root_folder: Path = Path.cwd()):
    """
    Redoes the shrinkwrapped faas function and yaml to ready it for google cloud build.
    """

    top_build: Path = get_cloud_build(root_folder)
    update_builds(root_folder)


# gs://dev-tooling/


@app.command(help="DEPRECIATED: Convert B64 to runnable file.")
def convert(
        target: ConvertTo = typer.Option(
            ...,
            help="Conversion target [Base64-> JSON] or [JSON -> Base64]",
            case_sensitive=False,
            show_choices=True),
        inputfile: typer.FileText = typer.
    Option(
        None,
        autocompletion=current_path_files,
        help="The input file. Can be left blank if converting to json file."),
        encoded: str = typer.Option(
            None,
            envvar=['GCP_SUPER_KEY', 'GCP_DOCKER_REGISTRY'],
            help="The input string for converting to json."),
        outputfile: typer.FileTextWrite = typer.Option(
            "output_file.txt",
            show_default=True,
            mode="w+",
            help="Where we save the result of the conversion.")):

    if target == ConvertTo.BASE:
        if not inputfile:

            typer.echo(
                "When converting into a base64, you need to supply a json file. Can't accept strings for formatting reasons."
            )

            iofile: str = typer.prompt("Please provide an input file",
                                       type=str)

            working = Path.cwd()
            input_dir = working / iofile
            inputfile: Path = input_dir
            logger.success(input_dir)
            logger.success(input_dir.exists())
            logger.success(input_dir.open().read())
            inputfile = input_dir.open()

        base_64_encoded = base64.b64encode(
            inputfile.read().encode()).decode('utf-8')

        typer.echo(f"File {inputfile.name} was converted into a base64:")
        typer.secho(base_64_encoded, fg=typer.colors.BRIGHT_BLUE)

        pyperclip.copy(base_64_encoded)

        outputfile.writelines(base_64_encoded)
        typer.echo(
            f"\n\nThe code was also saved to your clipboard and the following location: {outputfile.name}"
        )
    else:
        if encoded:
            original_text: str = base64.b64decode(encoded).decode('utf-8')
            typer.echo(
                f"Input string was converted into a base64. You should find it in the file: {outputfile.name}"
            )

            outputfile.writelines(original_text)
        else:
            is_file = typer.confirm(
                "There's no string. Would you like to use the file input instead?",
                default=True)
            if not is_file:
                raise typer.Exit(1)

            if not inputfile:
                updated_file: typer.FileText = typer.prompt(
                    "Please enter a file name you'd like to read from: ",
                    type=typer.FileText)
                original_text: str = base64.b64decode(
                    updated_file.read()).decode('utf-8')

                typer.echo(
                    f"File {inputfile.name} was converted into a base64. You should find it in the file: {outputfile.name}"
                )

                outputfile.write(original_text)
                # typer.secho(base_64_encoded, fg=typer.colors.BRIGHT_BLUE)


if __name__ == "__main__":
    app()
# gcloud auth activate-service-account --key-file=gcpcmdlineuser.json
