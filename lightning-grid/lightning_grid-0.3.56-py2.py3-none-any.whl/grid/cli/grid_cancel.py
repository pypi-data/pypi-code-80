import click

from grid import Grid


@click.group()
def cancel() -> None:
    pass


@cancel.command()
@click.argument('experiment_ids', type=str, required=True, nargs=-1)
def experiment(experiment_ids: [str]):
    client = Grid()
    for experiment in experiment_ids:
        client.cancel(experiment_id=experiment)


@cancel.command()
@click.argument('run_ids', type=str, required=True, nargs=-1)
def run(run_ids: [str]):
    client = Grid()
    for run in run_ids:
        client.cancel(run_name=run)
