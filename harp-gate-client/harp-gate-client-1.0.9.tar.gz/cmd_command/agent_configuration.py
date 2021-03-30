import click


@click.command()
@click.option("--monitoring-system", prompt="Choose monitoring system to configure", help="Monitoring system", type=click.Choice(['zabbix', 'icinga'], case_sensitive=False), required=True)
@click.option("--integration-name", prompt="Choose unique name of your integration", help="Name of your integration", required=True)
@click.option("--url", prompt="URL to your system (http://system-hostname)", help="http://system-hostname", required=True)
@click.option("--user", "-u", prompt="API Username", help="Username", required=True)
@click.option("--password", "-p", prompt="API User password", help="Password", required=True, hide_input=True, confirmation_prompt=True)
def agent_add(monitoring_system, integration_name, url, user, password):
    """Simple program that greets NAME for a total of COUNT times."""
    print("monitoring_system:", monitoring_system)
    print("monitoring_system:", integration_name)
    print("url:", url)
    print("user:", user)
    print("password:", password)


@click.command()
@click.option("--user", "-u", "user", prompt="API Username", help="Username", required=True)
def agent_update(user):
    """Simple program that greets NAME for a total of COUNT times."""
    print("user: ", user)


def agent_delete(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for _ in range(count):
        click.echo(f"Hello, {name}!")

