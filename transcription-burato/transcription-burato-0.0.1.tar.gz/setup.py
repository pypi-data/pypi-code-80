from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="transcription-burato",
    version="0.0.1",
    author="Otavio Burato de Oliveira",
    author_email="otavioburato42@gmail.com",
    description="A simples program that transcribes dna",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Otavio-Burato/DNA",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)
