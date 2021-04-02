import typer
from typing import Optional
from tabulate import tabulate
from proximatic import Proximatic
from .utils import item_table as item_table

app = typer.Typer()

proximatic = Proximatic()


@app.callback()
def callback():
    """
    --------------\n
    Welcome to Proximatic CLI!\n
    Interactive command-line interface for Proximatic.\n
    --------------\n
    """


@app.command()
def domain_list():
    """Returns a list of configured domains."""
    domains = proximatic.domain_list()["domains"]
    tabular = []
    for domain in domains:
        for name, url in domain.items():
            endpoint = name + "." + proximatic.get_fqdn()
            tabular.append([name, endpoint, url])
    table = tabulate(tabular, headers=["Name", "Endpoint", "URL"])
    typer.echo(f"\n{len(domains)} domains configured in Proximatic:\n")
    typer.echo(table)


@app.command()
def domain_fetch(subdomain: str = typer.Argument(..., help="The subdomain name of the domain to fetch.")):
    """Returns configuration settings for a given domain."""

    response = proximatic.domain_fetch(subdomain)
    if 'item' in response:
        table = item_table(response['item'])
        typer.echo(table)
    else:
        typer.echo("Domain not found.")


@app.command()
def domain_add(
    subdomain: str = typer.Option(..., prompt="Subdomain"),
    url: str = typer.Option(..., prompt="URL"),
):
    """Creates or replaces configuration for a given domain."""

    response = proximatic.domain_add(subdomain=subdomain, url=url)
    if response["result"] == "success":
        endpoint = subdomain + "." + proximatic.get_fqdn()
        table = tabulate(
            [[subdomain, endpoint, url]], headers=["Name", "Endpoint", "URL"]
        )
        typer.echo("Domain updated successfully.")
        typer.echo(f"\n{table}\n")
    else:
        raise typer.Exit(code=1)


@app.command()
def domain_delete(subdomain: str = typer.Argument(..., help="The domain to delete.")):
    """Deletes configuration for a given domain."""

    response = proximatic.domain_fetch(subdomain)
    if 'item' in response:
        table = item_table(response['item'])
        typer.echo(table)
        delete = typer.confirm("Are you sure you want to delete it?")
        if not delete:
            typer.echo("Not deleting")
            raise typer.Abort()
        task = proximatic.domain_delete(subdomain=subdomain)
        if task["result"] == "success":
            typer.echo(f"Successfully deleted {subdomain}.")
        else:
            typer.echo(response["result"])
            raise typer.Exit(code=1)
    else:
        typer.echo(response["result"])
        raise typer.Exit(code=1)
