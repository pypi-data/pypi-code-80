import click
from pyfiglet import Figlet

if __package__ is None or __package__ == '':
    from helper.click_helper import ClickHelper
    from helper.api_helper import ApiHelper
    from helper.click_helper import ConfigEntry
else:
    from cli.helper.click_helper import ClickHelper
    from cli.helper.api_helper import ApiHelper
    from cli.helper.click_helper import ConfigEntry


f = Figlet(font='big')
ascii_art = """
                  *@@@@@@@
                  *@@@@@@@
              .@@@@@@@@@@@@@@@@
              .@@@@@@@@@@@@@@@@
              .@@@@@@@@@@@@@@@@
                  *@@@@@@@
                  *@@@@@@@
                  *@@@@@@@
                  *@@@@@@@
                  *@@@@@@@
                  *@@@@@@@,         @@@@@
                   @@@@@@@@@@@@   @@@@@@@@
                    @@@@@@@@@@@   @@@@@@@@
                       @@@@@@@      #@@@
"""

@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    """traint CLI"""
    if ctx.invoked_subcommand is None:
        ClickHelper.echo_highlight(ascii_art)
        click.echo('Available commands')
        ClickHelper.echo_dual_color_highlight('status: ', 'Connection status traint API')
        ClickHelper.echo_dual_color_highlight('setup: ', 'Set config values for cluster communication')
        ClickHelper.echo_dual_color_highlight('usecase: ', 'List usecases')
        ClickHelper.echo_dual_color_highlight('data: ', 'Upload new data')
        ClickHelper.echo_dual_color_highlight('training: ', 'List existing trainings or start a new training')
        ClickHelper.echo_dual_color_highlight('model: ', 'List models')


##############################################################
# SETUP
##############################################################

@click.option('--api-base-url', default='https://api.traint.ai/v1', help='base url of the traint API', metavar='')
@click.option('--api-token', help='API token for your account', metavar='')
@click.group(invoke_without_command=True)
def setup(api_base_url, api_token):
    """Setup"""
    if ClickHelper.config_complete():
        ClickHelper.echo_highlight('Existing config found:')
        api_base_url = ClickHelper.get_config_value(ConfigEntry.API_BASE_URL)
        click.echo(f'Api base url: {api_base_url}')
        api_token = ClickHelper.get_config_value(ConfigEntry.API_TOKEN)
        click.echo(f'Api token: {api_token}')
    ClickHelper.prompt_config_values()

##############################################################
# GENERAL INFORMATION
##############################################################

@click.group(invoke_without_command=True)
def status():
    """API status"""
    try:
        status = ApiHelper.get_status()
        ClickHelper.echo_highlight(status)
    except ApiHelper.ConnectionError as err:
        ClickHelper.echo_error(err)


##############################################################
# USECASE MANAGEMENT
##############################################################

@click.group(chain=True, invoke_without_command=True)
@click.pass_context
def usecase(ctx):
    """Usecase Management"""
    if ctx.invoked_subcommand is None:
        click.echo('Usecase subcommands')
        ClickHelper.echo_dual_color_highlight('ls: ', 'List all usecases')
        ClickHelper.echo_dual_color_highlight('profile: ', 'Show data profiling for the latest training run')
        ClickHelper.echo_dual_color_highlight('logs: ', 'Show logs of usecase deployment')


@usecase.command()
def ls():
    """List all usecases"""

    usecases = []

    try:
        usecases = ApiHelper.get_usecases()
    except (ApiHelper.ConnectionError, ApiHelper.ServerError) as err:
        ClickHelper.echo_error(err)
        return

    if len(usecases) > 0:
        ClickHelper.echo_table(usecases)
    else:
        ClickHelper.echo_warning(f'No usecases created yet. It may take some minutes until your usecase will show up here. Start a training to launch your first usecase.')


@usecase.command()
@click.option('-u', '--usecase-name', prompt=True, required=True, help='name of the usecase', metavar='')
def profile(usecase_name):
    """Get the data profile for the latest usecase trainings run"""

    try:
        data_profile_url = ApiHelper.get_data_profile_url(usecase_name)
    except (ApiHelper.ConnectionError, ApiHelper.ServerError) as err:
        ClickHelper.echo_error(err)
        return

    ClickHelper.echo_dual_color_highlight(f'Latest data profile for usecase "{usecase_name}" can be accessed for 1 day using: ', data_profile_url)
    click.launch(data_profile_url)


@usecase.command()
@click.option('-u', '--usecase-name', prompt=True, required=True, help='name of the usecase', metavar='')
@click.option('-s', '--stage', prompt=True, required=True, help='stage of the deployment', metavar='')
def logs(usecase_name, stage):
    """Get the logs for a deployed usecase model"""

    try:
        logs = ApiHelper.get_usecase_logs(usecase_name, stage)
    except (ApiHelper.ConnectionError, ApiHelper.ServerError) as err:
        ClickHelper.echo_error(err)
        return

    if not logs:
        ClickHelper.echo_warning('No logs found.')
    else:
        click.echo(logs)


##############################################################
# DATA MANAGEMENT
##############################################################

@click.group(chain=True, invoke_without_command=True)
@click.pass_context
def data(ctx):
    """Data Management"""
    if ctx.invoked_subcommand is None:
        click.echo('Data subcommands')
        ClickHelper.echo_dual_color_highlight('ls: ', 'List uploaded data')
        ClickHelper.echo_dual_color_highlight('upload: ', 'Upload new data from CSV')


@data.command()
def ls():
    """List available training data"""

    data = []

    try:
        data = ApiHelper.get_data()
    except (ApiHelper.ConnectionError, ApiHelper.ServerError) as err:
        ClickHelper.echo_error(err)
        return

    if len(data) > 0:
        ClickHelper.echo_table(data)
    else:
        ClickHelper.echo_warning(f'No data uploaded yet.')


@data.command()
@click.option('-d', '--data-id', prompt=True, required=True, help='data id for referencing', metavar='')
@click.argument('file_path', type=click.Path(exists=True))
def upload(file_path, data_id):
    """Upload training data from CSV"""
    click.echo("Starting upload")

    try:
        response = ApiHelper.upload_data_file(file_path, data_id)
    except (ApiHelper.ConnectionError, ApiHelper.ServerError) as err:
        ClickHelper.echo_error(err)
        return

    ClickHelper.echo_highlight(f'Successfully uploaded data with ID "{response["data_id"]}"')


##############################################################
# TRAINING MANAGEMENT
##############################################################

@click.group(chain=True, invoke_without_command=True)
@click.pass_context
def training(ctx):
    """Training Management"""
    if ctx.invoked_subcommand is None:
        click.echo('Training subcommands')
        ClickHelper.echo_dual_color_highlight('ls: ', 'List trainings')
        ClickHelper.echo_dual_color_highlight('start: ', 'Start new training')
        ClickHelper.echo_dual_color_highlight('details: ', 'Show training details')


@training.command()
@click.option('-u', '--usecase-name', prompt=True, required=True, help='name of the usecase', metavar='')
def ls(usecase_name):
    """List all trainings"""

    trainings = []

    try:
        trainings = ApiHelper.get_trainings(usecase_name)
    except (ApiHelper.ConnectionError, ApiHelper.ServerError) as err:
        ClickHelper.echo_error(err)
        return

    if len(trainings) > 0:
        ordered_keys = ['id', 'status', 'start', 'runtime', 'metrics']
        ClickHelper.echo_table(trainings, ordered_keys)
    else:
        ClickHelper.echo_warning(f'No trainings for this usecase started yet.')


@training.command()
@click.option('-d', '--data-id', prompt=True, required=True, help='data id used when uploading', metavar='')
@click.option('-t', '--target', prompt=True, required=True, help='column to predict', metavar='')
@click.option('--trainer-type', hidden=True)
@click.option('-u', '--usecase-name', help='name of the usecase', metavar='')
@click.option('-o', '--options', help='json array of advanced training parameters', metavar='')
def start(data_id, target, trainer_type, usecase_name, options):
    """Start automated model training"""
    click.echo("\nStarting training...")

    try:
        usecase_name = ApiHelper.start_training(data_id, target, trainer_type, usecase_name, options)
    except (ApiHelper.ConnectionError, ApiHelper.ServerError) as err:
        ClickHelper.echo_error(err)
        return

    ClickHelper.echo_highlight(f'Successfully started training {usecase_name}')


@training.command()
@click.option('-u', '--usecase-name', prompt=True, required=True, help='name of the usecase', metavar='')
@click.option('-t', '--training-id', prompt=True, required=True, help='id of the trainings run', metavar='')
def details(usecase_name, training_id):
    """Show training details"""

    training_runs = []

    try:
        training_runs = ApiHelper.get_training_runs(usecase_name, training_id)
    except (ApiHelper.ConnectionError, ApiHelper.ServerError) as err:
        ClickHelper.echo_error(err)
        return

    if len(training_runs) > 0:
        ordered_keys = ['phase', 'name', 'runtime', 'metrics']
        ClickHelper.echo_table(training_runs, ordered_keys)
    else:
        ClickHelper.echo_warning(f'No training runs found.')


##############################################################
# MODEL MANAGEMENT
##############################################################

@click.group(chain=True, invoke_without_command=True)
@click.pass_context
def model(ctx):
    """Model Management"""
    if ctx.invoked_subcommand is None:
        click.echo('Model subcommands')
        ClickHelper.echo_dual_color_highlight('ls: ', 'List models')
        ClickHelper.echo_dual_color_highlight('details: ', 'Retrieve model details')
        ClickHelper.echo_dual_color_highlight('stage: ', 'Transition model to a different stage')


@model.command()
def ls():
    """List all models"""

    models = []

    try:
        models = ApiHelper.get_models()
    except (ApiHelper.ConnectionError, ApiHelper.ServerError) as err:
        ClickHelper.echo_error(err)
        return

    if len(models) > 0:
        ordered_keys = ['name', 'latest_version', 'staging_version', 'production_version', 'last_updated']
        ClickHelper.echo_table(models, ordered_keys)
    else:
        ClickHelper.echo_warning(f'No models created yet. Finish a training to see your first model.')


@model.command()
@click.option('-m', '--model-name', prompt=True, required=True, help='name of the model', metavar='')
def details(model_name):
    """Show model details"""

    try:
        model = ApiHelper.get_model(model_name)
    except (ApiHelper.ConnectionError, ApiHelper.ServerError) as err:
        ClickHelper.echo_error(err)
        return

    if model:
        ClickHelper.echo_property('name', model['name'])
        ClickHelper.echo_property('latest_version', model['latest_version'])
        ClickHelper.echo_property('staging_version', model['staging_version'])
        ClickHelper.echo_property('staging_prediction_url', model['staging_prediction_url'])
        ClickHelper.echo_property('production_version', model['production_version'])
        ClickHelper.echo_property('production_prediction_url', model['production_prediction_url'])
        ClickHelper.echo_property('last_updated', model['last_updated'])
    else:
        ClickHelper.echo_warning(f'No model found for this name.')


@model.command()
@click.option('-u', '--usecase-name', prompt=True, required=True, help='name of the usecase', metavar='')
@click.option('-v', '--version', prompt=True, required=True, help='model version to stage', metavar='')
@click.option('-s', '--stage', prompt=True, required=True, help='stage to transition model to', metavar='')
def stage(usecase_name, version, stage):
    """Stage model"""

    try:
        model = ApiHelper.stage_model(usecase_name, version, stage)
    except (ApiHelper.ConnectionError, ApiHelper.ServerError) as err:
        ClickHelper.echo_error(err)
        return

    ordered_keys = ['name', 'version', 'current_stage', 'last_updated', 'predict_url']
    ClickHelper.echo_table([model], ordered_keys)

def run_cli():
    if not ClickHelper.config_complete():
        ClickHelper.echo_error('CLI not setup yet.')
        ClickHelper.prompt_config_values()
        run_cli()
    else:
        main.add_command(setup)
        main.add_command(status)
        main.add_command(usecase)
        main.add_command(data)
        main.add_command(training)
        main.add_command(model)
        if __name__ == '__main__':
            main()

run_cli()
