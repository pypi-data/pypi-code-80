import click
from build_monitor_cli.main import main


@click.command()
@click.option('--org', required=True, help='organization alias in config file')
@click.option('--branch', default='master', help='filter branch, default: master')
def entry(org, branch):
    main(org, branch)

if __name__ == '__main__':
    entry()
