import setuptools
from pathlib import Path
setuptools.setup(
    name="Weight_convertor",
    version="1.0",
    packages=setuptools.find_packages(),
    long_description=Path("Readme.md").read_text()
)