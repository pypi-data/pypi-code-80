import inspect

import sh
import typer


class ShellCommands:
    @property
    def gcloud(self):
        try:
            return sh.Command("gcloud")
        except Exception as e:
            typer.secho("gcloud cli doesn't exist", fg='red', bold=True)
            raise typer.Exit(0)
