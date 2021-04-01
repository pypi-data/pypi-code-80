from .errors import AdsConfigError
from .utils import render_template

def config_inited(app, config):

    ads = config.ads

    if not isinstance(ads, dict) or not ads:

        raise AdsConfigError(
            "'ads' object must be properly defined in 'conf.py' file depending on a given vendor."
        )

    else:

        if 'vendor' not in ads.keys() or not ads['vendor']:

            raise AdsConfigError(
                "'vendor' must be defined, supported values: 'carbonads' or 'ethicalads'."
            )

        elif ads['vendor'] not in ['carbonads', 'ethicalads']:

            raise AdsConfigError(
                f"'{ads['vendor']}' is not recognized as vendor's value, supported values: 'carbonads' or 'ethicalads'."
            )

        else:

            if 'attributes' not in ads.keys() or not isinstance(ads['attributes'], dict) or not ads['attributes']:

                raise AdsConfigError(
                    f"{ads['vendor']}: 'attributes' must be properly defined according to the given vendor."
                )

            else:

                if ads['vendor'] == 'carbonads':

                    if 'url' not in ads['attributes'].keys() or not ads['attributes']['url']:
                        raise AdsConfigError(
                            "carbonads: 'url' must be defined."
                        )

                elif ads['vendor'] == 'ethicalads':

                    if 'data-ea-publisher' not in ads['attributes'].keys() or not ads['attributes']['data-ea-publisher']:
                        raise AdsConfigError(
                            "ethicalads: 'data-ea-publisher' must be defined."
                        )

def html_page_context(app, pagename, templatename, context, doctree):

    def ads():

        ads = app.config.ads

        if ads['vendor'] == 'carbonads':
            str = '<script async src="{{ attributes.url }}" id="_carbonads_js"></script>'

        elif ads['vendor'] == 'ethicalads':
            str = """<script async src="https://media.ethicalads.io/media/client/ethicalads.min.js"></script>
                     <div {% if attributes['class'] %}class="{{ attributes['class'] }}"{% endif %}
                          {% if attributes['id'] %}id="{{ attributes['id'] }}"{% endif %}
                          data-ea-publisher="{{ attributes['data-ea-publisher'] }}"
                          {% if attributes['data-ea-type'] %}data-ea-type="{{ attributes['data-ea-type'] }}"{% endif %}
                          {% if attributes['data-ea-keywords'] %}data-ea-keywords="{{ attributes['data-ea-keywords'] }}"{% endif %}
                          {% if attributes['data-ea-campaign-types'] %}data-ea-campaign-types="{{ attributes['data-ea-campaign-types'] }}"{% endif %}
                          {% if attributes['data-ea-manual'] %}data-ea-manual="{{ attributes['data-ea-manual'] }}"{% endif %}></div>"""

        ctx = {'attributes': ads['attributes']}
        return render_template(str, ctx)


    context['ads'] = ads
