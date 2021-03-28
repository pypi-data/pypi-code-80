from setuptools import setup


def find_value(key):
    from pathlib import Path
    import re
    re_str = """%s[\s]*?=[\s]*?[\"\'\[\(\{ ]*(?P<val>.*)[\"\'\]\)\} ]"""
    this_dir = Path('.').absolute()
    re_str %= key
    for file in this_dir.rglob('*.py'):
        for item in re.finditer(re_str, file.read_text()):
            return item['val'].strip()


setup(
    name="scrapertools",
    version=find_value('__version__'),
    packages=["scrapertools"],
    url=find_value('__url__'),
    license=find_value('__license__'),
    author=find_value('__author__'),
    author_email=find_value('__author_email__'),
    description=find_value('__description__'),
    install_requires=[
        "requests",
    ],
    extras_require={
        "video": ["m3u8"]
    },
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
