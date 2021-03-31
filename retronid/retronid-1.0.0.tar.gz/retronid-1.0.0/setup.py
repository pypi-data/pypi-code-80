import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="retronid",
    version="1.0.0",
    description="A short unique id.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/retronbv/retronid-py",
    author="retronbv",
    author_email="retronbv@gmail.com",
    license="MIT",
    install_requires=["uuid"],
    include_package_data=True,
)