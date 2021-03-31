import webbrowser
import sys
import os.path

import click
import click_config_file
import toml

from zeddo.news import get_top_news


def show_top_news(top_news):
    for i, article in enumerate(top_news):
        title = article['title']
        source = article['source']['name']
        click.echo('{} {} {}'.format(
            click.style('[{}]'.format(i+1), bold=True),
            title,
            click.style('({})'.format(source), dim=True)
        ))


def open_article(top_news, n):
    article = top_news[n - 1]
    webbrowser.open(article['url'])


@click.command()
@click.option('--api-key', help='API key for News API')
@click.option('--language', default='en')
@click.option('-n', '--max-count', default=5)
@click_config_file.configuration_option(cmd_name='zeddo')
def top_news(api_key, language, max_count):
    # Prompt for API key if not supplied
    if api_key is None:
        api_key = click.prompt('Enter your API key')
        if click.confirm('Save to config file?', default='y'):
            config_path = os.path.join(
                click.get_app_dir(app_name='zeddo'),
                'config'
            )
            # Write to config
            with open(config_path, 'w+') as c:
                config = toml.load(c)
                config['api_key'] = api_key
                toml.dump(config, c)
                print('Saved!\n')

    # Fetch news
    top_news = get_top_news(api_key, language, max_count)
    # Display news
    show_top_news(top_news)

    # Prompt for selection and open it in web browser
    i = None
    while True:
        s = click.prompt(
            'Please enter an article number to open',
            default='',
            show_default=False
        )
        # Quit on empty input
        if s == '':
            sys.exit(0)

        # Validate input
        if not s.isnumeric():
            click.echo('{} is not a number!'.format(s))
        else:
            i = int(s)
            if not (0 < i <= len(top_news)):
                click.echo('No such article: {}'.format(i))
            else:
                break

    open_article(top_news, i)


if __name__ == '__main__':
    top_news()
