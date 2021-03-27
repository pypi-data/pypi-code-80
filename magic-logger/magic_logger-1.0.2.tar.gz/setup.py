import os

from setuptools import setup

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), "r") as f:
    long_description = f.read()

description = "This very simple module does its best to help you use Python's logging correctly, by making sure you always invoke the right Logger for a module."

setup(
    name="magic_logger",
    packages=["magic_logger"],
    package_data={
        "magic_logger": ["py.typed"]
    },
    version="1.0.2",
    license="MIT",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Radu Ghitescu",
    author_email="radu.ghitescu@gmail.com",
    url="https://github.com/RaduG/magic_logger",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.6",
    zip_safe=False,
)
