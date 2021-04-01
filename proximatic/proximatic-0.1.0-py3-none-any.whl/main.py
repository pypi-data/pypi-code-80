import typer
from typing import Optional
import proximatic


app = typer.Typer()


@app.callback()
def callback():
    """
    Proximatic CLI\n
    Manage your Proximatic configuration files.
    """


@app.command()
def domain_list():
    """Returns a list of configured domains."""
    manager = proximatic.DomainsManager()
    result = manager.domain_list()
    typer.echo("Domains:\n--------")
    for domain in result["domains"]:
        for name, url in domain.items():
            typer.echo(f"{name}.example.com <=proxy=> {url}")


@app.command()
def domain_update(
    subdomain: str = typer.Option(..., prompt="Subdomain"),
    url: str = typer.Option(..., prompt="URL"),
):
    """Creates or replaces a domain configuration .yml file."""

    manager = proximatic.DomainsManager()
    response = manager.domain_update(subdomain = subdomain, url = url)
    if response['result'] == "success":
        typer.echo("Domain updated successfully.")
        typer.echo(f"{manager.proximatic_fqdn}.{subdomain} => {url}")
    else:
        raise typer.Exit(code=1)

@app.command()
def domain_delete(
    subdomain: str = typer.Option(..., prompt="Subdomain"),
):
    manager = proximatic.DomainsManager()
    response = manager.domain_delete(subdomain = subdomain)
    if response['result'] == "success":
        typer.echo(f"Domain {subdomain} was deleted successfully.")
    else:
        typer.echo(response['result'])
        raise typer.Exit(code=1)