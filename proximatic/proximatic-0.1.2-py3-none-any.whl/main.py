import typer
from typing import Optional
from proximatic import Proximatic


app = typer.Typer()

proximatic = Proximatic()


@app.callback()
def callback():
    """
    Proximatic CLI\n
    Manage your Proximatic configuration files.
    """


@app.command()
def domain_list():
    """Returns a list of configured domains."""
    domains = proximatic.domain_list()["domains"]
    typer.echo("Domains:\n--------")
    for domain in domains:
        for name, url in domain.items():
            typer.echo(f"{name}.example.com <=proxy=> {url}")


@app.command()
def domain_update(
    subdomain: str = typer.Option(..., prompt="Subdomain"),
    url: str = typer.Option(..., prompt="URL"),
):
    """Creates or replaces a domain configuration .yml file."""
    response = proximatic.domain_update(subdomain=subdomain, url=url)
    if response["result"] == "success":
        typer.echo("Domain updated successfully.")
        typer.echo(f"{subdomain}.{proximatic.proximatic_fqdn} => {url}")
    else:
        raise typer.Exit(code=1)


@app.command()
def domain_delete(
    subdomain: str = typer.Option(..., prompt="Subdomain"),
):
    response = proximatic.domain_delete(subdomain=subdomain)
    if response["result"] == "success":
        typer.echo(f"Domain {subdomain} was deleted successfully.")
    else:
        typer.echo(response["result"])
        raise typer.Exit(code=1)
