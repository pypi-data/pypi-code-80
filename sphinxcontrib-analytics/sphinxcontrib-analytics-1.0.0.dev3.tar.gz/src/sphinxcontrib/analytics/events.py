from .errors import AnalyticsConfigError
from .utils import render_template


def config_inited(app, config):

    analytics = config.analytics

    if not analytics or not isinstance(analytics, dict):

        raise AnalyticsConfigError(
            "'analytics' object must be properly defined in 'conf.py' file depending on a given list of vendor(s)."
        )

    else:

        if 'enable' not in analytics.keys() or not (analytics['enable'] and isinstance(analytics['enable'], list) and all(isinstance(item, str) for item in analytics['enable'])):

            raise AnalyticsConfigError(
                "'enable' must be a list of one or more supported vendors: 'google', 'matomo'."
            )

        elif not any(item in analytics['enable'] for item in ['google', 'matomo']):

            raise AnalyticsConfigError(
                "you must enable at least one of supported vendor(s): 'google', 'matomo'."
            )

        else:

            if 'vendors' not in analytics.keys() or not (analytics['vendors'] and isinstance(analytics['vendors'], dict)):

                raise AnalyticsConfigError(
                    "'vendors' must be a dictionnary of valid vendor(s) config object(s)."
                )

            elif not any(item in analytics['vendors'].keys() for item in ['google', 'matomo']):

                raise AnalyticsConfigError(
                    "no supported vendor(s) config object(s) were found."
                )

            else:

                if 'google' in analytics['enable']:

                    if 'google' not in analytics['vendors'].keys() or not (analytics['vendors']['google'] and isinstance(analytics['vendors']['google'], dict)):

                        raise AnalyticsConfigError(
                            "'google' vendor config object is missing or missconfigured."
                        )

                    else:

                        if 'tracking_id' not in analytics['vendors']['google'].keys() or not analytics['vendors']['google']['tracking_id']:

                            raise AnalyticsConfigError(
                                "'tracking_id' must be defined for vendor 'google' following this pattern: 'UA-XXXXX-Y'."
                            )

                if 'matomo' in analytics['enable']:

                    if 'matomo' not in analytics['vendors'].keys() or not (analytics['vendors']['matomo'] and isinstance(analytics['vendors']['matomo'], dict)):

                        raise AnalyticsConfigError(
                            "'matomo' vendor config object is missing or missconfigured."
                        )

                    else:

                        if 'matomo_url' not in analytics['vendors']['matomo'].keys() or not analytics['vendors']['matomo']['matomo_url']:

                            raise AnalyticsConfigError(
                                "'matomo_url' must be defined for vendor 'matomo' without http/https schema, e.g: 'matomo.example.com'."
                            )

def enqueue_script(app, pagename, templatename, context, doctree):

    analytics = app.config.analytics

    metatags = context.get('metatags', '')

    if 'google' in analytics['enable']:
        metatags += render_template(
            'google-analytics.html',
            {'tracking_id': analytics['vendors']['google']['tracking_id']}
        )

    if 'matomo' in analytics['enable']:
        metatags += render_template(
            'matomo-analytics.html',
            {'matomo_url': analytics['vendors']['matomo']['matomo_url']}
        )

    context['metatags'] = metatags
