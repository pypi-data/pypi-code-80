from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'The simplest encryption module for Python :)'
LONG_DESCRIPTION = open("README.md", "r", encoding="utf-8").read()

setup(
    name="cryptous",
    version=VERSION,
    author="Guimov",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    package=find_packages(),
    classifiers=[
    	"Development Status :: 4 - Beta",
    	"Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Telecommunications Industry",
        "Programming Language :: Python",
        "Topic :: Security",
        "Topic :: Security :: Cryptography"
    ]
)