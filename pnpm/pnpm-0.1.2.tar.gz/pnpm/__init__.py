from rich import print
from . import install
__version__ = '0.1.1'


def whoisthis():
    print(f"This is {__version__}")
    
def install():
    install.install()

