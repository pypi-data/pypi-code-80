from docutils.parsers.rst import Directive, directives

from .nodes import AdsJavascriptNode, AdsPlacementNode


class AdsDirective(Directive):
    """Ads ".. ads::" rst directive."""

    def run(self):

        ads = self.state.document.settings.env.config.ads

        if ads['vendor'] == 'carbonads':
            return [AdsJavascriptNode(ads=ads)]
        elif ads['vendor'] == 'ethicalads':
            return [AdsJavascriptNode(ads=ads), AdsPlacementNode(ads=ads)]
