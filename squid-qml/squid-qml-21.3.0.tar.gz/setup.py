from setuptools import setup

__version__ = "21.3.0"

with open('requirements.txt') as f:
    required = f.read().splitlines()


with open('README.md') as f:
    README = f.read()

setup(
    name="squid-qml",
    version=__version__,
    author="Jakub Filipek",

    description="SQUID: Hybrid Quantum-Classical ML package",
    long_description_content_type="text/markdown",
    long_description=README,

    url="https://bitbucket.org/squid-qml/squid",

    packages=["squid"],
    install_requires=required,
)
