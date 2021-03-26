from setuptools import setup
from urllib.request import urlopen
from urllib.error import HTTPError
import json

with open('README.md', 'r') as f:
    read = f.read()


package = 'py_temp'


class Version:
    def __init__(self, digits, base=10):
        self.digits = [int(x) for x in digits]
        self.base = base
    
    def update(self):
        digits = self.digits[::-1]
        for i, digit in enumerate(digits):
            digits[i] = digit % self.base
            next = (digit - digit % self.base)/self.base
            if next > 0:
                try:
                    digits[i + 1] = int(next)
                except IndexError:
                    digits.append(int(next))
        self.digits = digits[::-1]

    def up(self):
        self.digits[-1] += 1
        self.update()
    
    def __str__(self):
        return '.'.join([str(x) for x in self.digits])


def next_version(base=10):
    try:
        resp = urlopen('https://pypi.org/pypi/PythonTemplates/json')
        versions = list(json.loads(resp.read())['releases'].keys())
        latest = versions[-1]
        version = Version(latest.split('.'), base)
        return str(version)
    except (HTTPError, IndexError):
        return '0.0.0'


setup(
    name=package.replace('_', '-'),
    description='A CLI tool for rendering python code using Jinja2.',
    long_description=read,
    long_description_content_type='text/markdown',
    version=next_version(),
    url='https://github.com/TeamNightSky/PyTemp',
    author='FoxNerdSaysMoo, GrandMoff100',
    author_email='teamnightsky.gh@gmail.com',
    install_requires=['jinja2', 'toml', 'click'],
    packages=[package],
    entry_points = {
        'console_scripts': [f"{package.replace('_','')}={package}.cli:cli"],
    }
)
