import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

README = (HERE / 'README.md').read_text()

setup(
    name = 'ServerCL',
    author = 'Shaun Cameron',
    author_email = 'shauncameron1303@gmail.com',
    version= '0a',
    description = 'Create a simple yet effective server with and connect to it with a simple client!',
    long_description = README,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/shauncameron/server-server_client',
    license = 'MIT', 
    packages = find_packages()
)

print(' Packages Loaded >>', find_packages())