from . import v1
from . import v2
from .server import run_simple, create_app

__author__ = """Yossi Mosbacher"""
__email__ = 'joe.mosbacher@gmail.com'
__version__ = '0.1.3'

VERSIONS = {
    "v1": v1,
    "v2": v2,
}

DEFAULT_VERSION = "v2"

def get_server(version, **kwargs):
    app = VERSIONS[version].app.make_app(**kwargs)
    return app

def default_server():
    return get_server(DEFAULT_VERSION)

