from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="fuego",
    version='0.0.1',
    author="Nathan Raw",
    author_email="naterawdata@gmail.com",
    description="Tools for running experiments in the cloud",
    license="MIT",
    install_requires=requirements,
    packages=find_packages(),
    entry_points={
        'console_scripts': ['fuego=fuego.cli:app'],
    }
)
