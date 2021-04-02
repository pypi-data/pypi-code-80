from setuptools import find_packages
from setuptools import setup
from pip._internal.req import parse_requirements
import os

with open("README.md", "r") as fh:
    long_description = fh.read()


# Pulls pip packages with versions from the requirements file
install_requires = parse_requirements("requirements.txt", session="snowchange")
test_requires = parse_requirements("requirements.txt", session="snowchnage")

setup(
    name="snowchange",
    version="2.8.1",
    description="snowchange is now schemachange",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["schemachange"],
    classifiers=["Development Status :: 7 - Inactive"],
)
