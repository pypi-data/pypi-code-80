VERSION = (1, 0, 0, 'dev0')
__version__ = '.'.join(map(str, VERSION))

from .directives import AdsDirective
from .events import config_inited, html_page_context
from .nodes import AdsJavascriptNode, AdsPlacementNode


def setup(app):

    app.add_config_value('ads', None, True)
    app.add_node(AdsJavascriptNode, html=(AdsJavascriptNode.visit, AdsJavascriptNode.depart))
    app.add_node(AdsPlacementNode, html=(AdsPlacementNode.visit, AdsPlacementNode.depart))
    app.add_directive('ads', AdsDirective)

    app.connect('config-inited', config_inited)
    app.connect('html-page-context', html_page_context)

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
