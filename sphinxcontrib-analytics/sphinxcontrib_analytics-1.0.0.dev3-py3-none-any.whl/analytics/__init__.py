VERSION = (1, 0, 0, 'dev3')
__version__ = '.'.join(map(str, VERSION))

from .events import config_inited, enqueue_script


def setup(app):
    app.add_config_value('analytics', None, True)
    app.connect('config-inited', config_inited)
    app.connect('html-page-context', enqueue_script)

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True
    }
