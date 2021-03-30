from os import path

from setuptools import find_packages
from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    install_requires = f.read().splitlines()

setup(
    name="derezzed",
    version="0.0a2",
    packages=find_packages(exclude=['docs']),
    install_requires=install_requires,
    author="Iain R. Learmonth",
    author_email="irl@sr2.uk",
    description=("A toolkit for reducing data resolution for privacy-preserving"
                 " applications"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="privacy metrics analytics",
    url="https://gitlab.com/cleaninsights/derezzed",
    project_urls={
        "Bug Tracker": "https://gitlab.com/cleaninsights/derezzed/-/issues",
        "Source Code": "https://gitlab.com/cleaninsights/derezzed",
    },
    classifiers=["License :: OSI Approved :: BSD License"],
    test_suite='nose.collector',
)
