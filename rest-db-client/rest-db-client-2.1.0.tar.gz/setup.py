from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='rest-db-client',
    version='2.1.0',
    author_email="info@librecube.org",
    description='Client for RESTful databases',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/librecube/lib/python-rest-db-client",
    license="MIT",
    python_requires='>=3',
    packages=find_packages(),
    install_requires=['requests'],
)
