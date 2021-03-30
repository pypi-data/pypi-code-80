# This Python file uses the following encoding: utf-8
from setuptools import setup, find_packages

setup(  name='csv_dispatcher',
        packages=find_packages(),
        version='0.0.1',
        description='Description.',
        long_description='Run dispatcher.',
        author='MatteoLacki',
        author_email='matteo.lacki@gmail.com',
        url='https://github.com/MatteoLacki/csv_dispatcher.git',
        keywords=['Great module', 'Devel Inside'],
        classifiers=['Development Status :: 1 - Planning',
                     'License :: OSI Approved :: BSD License',
                     'Programming Language :: Python :: 3.6',
                     'Programming Language :: Python :: 3.7'],
        install_requires=['pandas'],
        scripts = [
            'bin/csv_dispatch.py'
        ]
)
