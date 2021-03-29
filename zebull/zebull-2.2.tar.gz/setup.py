import setuptools
import os
import io
from setuptools import setup


with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="zebull",
    version="2.2",
    author="Stoneage Solutions",
    author_email="pradeep@stoneagesolutions.com",
    description="Python SDK for API users",
    license="MIT",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://zebull.in",
    downloadable_url="https://github.com/jerokpradeep/pythonZebullAPI",
    packages=["zebullconnect"],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Intended Audience :: Developers",
    ],

    python_requires='>=3.0'
)