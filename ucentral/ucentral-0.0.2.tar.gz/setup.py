import io

from setuptools import find_packages, setup
from os.path import dirname, abspath, join


with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

base_path = dirname(abspath(__file__))

with open(join(base_path, "requirements.txt")) as req_file:
    requirements = req_file.readlines()

setup(
    name="ucentral",
    version="0.0.2",
    url="https://github.com/aparcar/ucentral-cli",
    maintainer="Paul Spooren",
    maintainer_email="mail@aparcar.org",
    description="CLI to create ucentral configuration files",
    entry_points={
        "console_scripts": ["ucentral=ucentral.cli:loop"],
    },
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
)
