import requests

# Cache list of all news sources
all_sources = None


def get_sources(api_key):
    url = 'https://newsapi.org/v2/sources?apiKey={}'.format(api_key)

    response = requests.request('GET', url)
    if response.status_code != 200:
        raise RuntimeError(response.json()['message'])

    return response.json()['sources']


def get_top_news(api_key, language, category, query, n):
    global all_sources
    if all_sources is None:
        all_sources = [source['id'] for source in get_sources(api_key)]

    # Since `sources` (or `country` or `q`) is required, provide all sources.
    url = (
        'https://newsapi.org/v2/top-headlines?' +
        'apiKey={}&'.format(api_key) +
        'language={}&'.format(language) +
        # Cannot provide both `sources` and `category` for whatever reason
        ('sources={}&'.format(','.join(all_sources)) if not category else '') +
        ('category={}&'.format(category) if category else '') +
        ('q={}&'.format(query) if query else '') +
        'pageSize={}'.format(n)  # no need for more than n entries
    )

    response = requests.request('GET', url)
    if response.status_code != 200:
        raise RuntimeError(response.json()['message'])

    articles = response.json()['articles']
    return articles[:n] if n < len(articles) else articles
