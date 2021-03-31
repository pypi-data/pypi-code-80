import click
import validators
import harp_agent.settings as settings
import json
import os
import errno


def is_root(ctx, param, value):
    if not value:
        ctx.abort()

    if os.geteuid() == 0:
        return True
    else:
        raise click.BadParameter("""
        ==========================
        You should run command from root user!!!
        ==========================
        """)


def validate_url(ctx, param, value):
    if validators.url(value):
        return value
    else:
        raise click.BadParameter(f'Wrong URL: {value}. Should be in format like - http://system-hostname')


def update_config_file(new_config):
    # Read file
    with open(settings.PATH_TO_MS_CONFIG) as json_file:
        data = json.load(json_file)

    # Prepare config to insert
    unique_integration = f"{new_config['monitoring_system']}_{new_config['integration_name']}"
    if unique_integration in data:
        print(f'Integration - "{unique_integration}" already exist in configuration - {settings.PATH_TO_MS_CONFIG}')
    else:
        data[unique_integration] = new_config

    # Update file
    with open(settings.PATH_TO_MS_CONFIG, 'w') as outfile:
        json.dump(data, outfile)


@click.command()
@click.option('--yes', is_flag=True, callback=is_root, expose_value=False, prompt='Are you running command from root?')
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
