import itertools
import sys

import log
import pomace
import typer
from bullet import Bullet

from .scripts import Script


def run():
    typer.run(cli)


def cli(
    names: list[str] = typer.Argument(
        None,
        metavar="[SCRIPT SCRIPT ...]",
        help="Names of one or more scripts to run in a loop",
    ),
    iterations: int = typer.Option(10, help="Iterations to spend in each script"),
    dev: bool = typer.Option(False, help="Enable development mode"),
):
    log.init()

    scripts = {}
    for cls in Script.__subclasses__():
        script = cls()
        scripts[script.name] = script

    choices = list(scripts.keys())
    if "all" in names:
        log.info("Running all scripts")
        names = choices

    cli = Bullet(prompt="\nSelect a script to run:", bullet=" ● ", choices=choices)
    if not all(name in choices for name in names) or not names:
        names = [cli.launch()]
        pomace.prompts.linebreak(force=True)

    try:
        import caffeine
    except ImportError:
        log.warn(f"Display sleep cannot be disabled on {sys.platform}")
    else:
        caffeine.on(display=True)

    pomace.utils.locate_models()
    if not dev:
        pomace.freeze()

    try:
        _run(scripts, names, iterations)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        log.error(e)
        if dev:
            breakpoint()
        else:
            raise e from None


def _run(scripts: dict, names: list, iterations: int):
    if len(names) > 1:
        for count in itertools.count(start=1):
            for name in names:
                scripts[name].loop(iterations * count)
    else:
        scripts[names[0]].loop()
