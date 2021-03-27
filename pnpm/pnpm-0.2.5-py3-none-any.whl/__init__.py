from rich import print
from install import install as i

__version__ = '0.2.1'

def whoisthis():
    print(f"This is {__version__}")
    
def install():
    i.install()
