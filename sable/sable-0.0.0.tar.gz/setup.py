from setuptools import setup
from sable import __version__


with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="sable",
    version=".".join(str(version) for version in __version__),
    description="Sable is a testing tool for SQL.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HH-MWB/sable",
    author="HH-MWB",
    author_email="h.hong@mail.com",
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing"
    ],
    packages=["sable"],
)
