from setuptools import setup, find_packages
import codecs
import os

LONG_DESCRIPTION = '''
    read the docs on my website!
    https://sites.google.com/view/mst-creator-docs/memes-and-jokes-docs
'''

# Setting up
setup(
    name="memes-and-jokes",
    version="0.0.1",
    author="MST_Creator_Dev",
    author_email="tssab.creator@gmail.com",
    description="Gets memes and jokes from Reddit",
    long_description_content_type="text/markdown",
    long_description = LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'memes', 'jokes', 'praw', 'PRAW', 'reddit', 'Reddit'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)