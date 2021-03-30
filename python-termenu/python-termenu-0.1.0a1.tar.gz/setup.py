# Modules
import os
import pathlib
from setuptools import setup

# Grab our current path
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding = "utf-8")

# Package finder
def find_packages(dir):
    packs = []
    for p, _, __ in os.walk(dir):
        path = p.replace("\\", "/").replace("/", ".").replace(dir + ".", "")
        if "egg-info" not in path and "__pycache__" not in path:
            if path != dir:
                packs.append(path)
                print(path)

    return packs

# Handle setup
setup(
    name = "python-termenu",
    version = "0.1.0a-1",
    description = "Simple terminal-based menus in Python",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/ii-Python/termenu",
    author = "iiPython",
    author_email = "ben@iipython.cf",
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",

        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords = "menu, terminal, cli",
    package_dir = {"": "src"},
    packages = find_packages("src"),
    python_requires = ">=3.6, <4",
    project_urls = {
        "Bug Reports": "https://github.com/ii-Python/termenu/issues",
        "Source": "https://github.com/ii-Python/termenu/",
    }
)
