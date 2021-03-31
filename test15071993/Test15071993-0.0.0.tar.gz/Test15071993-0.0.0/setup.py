from setuptools import setup
import setuptools

long_description = open('README.md').read()

setup(
    name='Test15071993',
    version='0.0.0',
    url="https://github.com/kshamashuttl",
    author="Kshama Singh",
    author_email="kshama.singh@shuttl.com",
    description="A Command Line Interface",
    packages=setuptools.find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['Test15071993'],
    entry_points='''
        [console_scripts]
        autoT=autoT:cli
    '''
)