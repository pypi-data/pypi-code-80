# entry point to bot

from telewater.bot import run_single_bot
from telewater import __version__, __doc__
import typer

app = typer.Typer(add_completion=False)


@app.command()
def start(name: str, token: str):
    ''' Run the bot with the username NAME and TOKEN obtained from @BotFather
    '''
    print(f'telewater v{__version__}\n{__doc__}')
    run_single_bot(name, token)
