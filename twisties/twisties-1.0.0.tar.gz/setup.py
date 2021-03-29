import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="twisties",
    version="1.0.0",
    description="Twisty puzzle scrambler for python",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Adog64/twisties",
    author="Aidan Sharpe",
    author_email="amsharpe102@protonmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["twisties"],
    include_package_data=True)