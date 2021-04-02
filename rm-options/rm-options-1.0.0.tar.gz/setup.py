import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="rm-options",
    version="1.0.0",
    description="python package for easy cli options handling",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/MartinR2295/rm-options",
    author="Martin Rader",
    author_email="m1rader@edu.aau.at",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["rmoptions", "rmoptions.mapper"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": []
    },
)