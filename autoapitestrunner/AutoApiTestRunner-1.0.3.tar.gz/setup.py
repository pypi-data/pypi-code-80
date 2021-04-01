from setuptools import setup
import setuptools


long_description = open('README.md').read()


setup(
    name='AutoApiTestRunner',
    version='1.0.3',
    url="https://github.com/kshamashuttl",
    author="Kshama Singh",
    author_email="kshama.singh@shuttl.com",
    description="A Command Line Interface to run Shuttl API tests",
    packages=setuptools.find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['AutoApiTestRunner'],
    install_requires=[
        'Click', 'Requests',
    ],
    entry_points='''
        [console_scripts]
        auto=AutoApiTestRunner.auto:cli
    '''
)