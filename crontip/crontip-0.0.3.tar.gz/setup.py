"""Setup to build distribution"""


# Standard library import
import pathlib

# Third party library
from setuptools import setup

# Local import
from crontip.__version__ import __version__

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / 'README.md').read_text()

setup(
    name='crontip',
    version=f'{__version__}',
    description='Backup, edit and install crontab',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/shangcode/crontip',
    author='shangcode',
    author_email='shangcode@aliyun.com',
    license='CLA',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Archiving :: Backup'
    ],
    packages=['crontip'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'crontip=crontip.__main__:main'
        ]
    }
)
