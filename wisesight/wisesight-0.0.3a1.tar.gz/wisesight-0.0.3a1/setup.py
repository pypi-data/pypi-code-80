from setuptools import setup, find_packages
import pathlib
import os
from setuptools import setup

# The directory containing this file
CURRENT_DIR = pathlib.Path(__file__).parent

setup(
    name='wisesight',
    version='0.0.3-alpha1',
    url='https://github.com/plutonyx/wisesight',
    author='Thaweesak Chusri',
    author_email='p4l3k1n6@gmail.com',
    description='The wisesight social listening project',
    long_description=open(os.path.join(CURRENT_DIR, "README.md")).read(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=[],    
    include_package_data=True,
    install_requires=[],
)
