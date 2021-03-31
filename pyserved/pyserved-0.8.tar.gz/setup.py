import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pyserved",
    version="0.8",
    description="Share files (UTF-8) through your network. (multi-paltform)",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/shaurya-blip/pyserved/",
    author="Shaurya Pratap Singh",
    author_email="shaurya.p.singh21@gmail.com",
    license="MIT",
    packages=["pyserved"],
    include_package_data=True,
    scripts=['bin/pyserved', 'bin/pyserved-c'],
)


