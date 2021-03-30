from setuptools import setup, find_packages
import codecs
import os

LONG_DESCRIPTION = '''
DEPENDENCIES: urllib and re (both are default and come with python)

USE:

```
from YT_Searcher import yt_searcher as yt

print(yt.watch('python'))
```
'''

# Setting up
setup(
    name="yt-searcher-for-py",
    version="0.0.2",
    author="MST_Creator_Dev",
    author_email="tssab.creator@gmail.com",
    description="Searches youtube for videos and returns the link of the first result",
    long_description_content_type="text/markdown",
    long_description = LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'youtube', 'searcher', 'video'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)