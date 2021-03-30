import click
import validators
import harp_gate_client.settings as settings
import json
import os
import errno


def validate_url(ctx, param, value):
    if validators.url(value):
        return value
    else:
        raise click.BadParameter(f'Wrong URL: {value}. Should be in format like - http://system-hostname')


def update_config_file(data):
    if not os.path.exists(os.path.dirname(settings.PATH_TO_MS_CONFIG)):
        try:
            os.makedirs(os.path.dirname(settings.PATH_TO_MS_CONFIG))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    try:
        with open(settings.PATH_TO_MS_CONFIG, 'w') as outfile:
            print(outfile, data)
            json.dump(data, outfile)
    except FileNotFoundError:
        with open(settings.PATH_TO_MS_CONFIG, 'w+') as outfile:
            json.dump(data, outfile)



@click.command()
@click.option("--monitoring-system", prompt="Choose monitoring system to configure", help="Monitoring system", type=click.Choice(['zabbix', 'icinga'], case_sensitive=False), required=True)
@click.option("--integration-name", prompt="Choose unique name of your integration", help="Name of your integration", required=True)
@click.option("--url", prompt="URL to your system (http://system-hostname)", help="http://system-hostname", required=True, callback=validate_url)
@click.option("--user", "-u", prompt="API Username", help="Username", required=True)
@click.option("--password", "-p", prompt="API User password", help="Password", required=True, hide_input=True, confirmation_prompt=True)
def agent_add(monitoring_system, integration_name, url, user, password):
    """Simple program that greets NAME for a total of COUNT times."""
    config = {
        'monitoring_system': monitoring_system,
        'integration_name': integration_name,
        'url': url,
        'user': user,
        'password': password
    }
    update_config_file(config)


@click.command()
@click.option("--user", "-u", "user", prompt="API Username", help="Username", required=True)
def agent_update(user):
    """Simple program that greets NAME for a total of COUNT times."""
    print("user: ", user)


def agent_delete(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for _ in range(count):
        click.echo(f"Hello, {name}!")
