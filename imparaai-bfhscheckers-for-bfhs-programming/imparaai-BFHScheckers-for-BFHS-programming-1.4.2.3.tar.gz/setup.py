import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "imparaai-BFHScheckers-for-BFHS-programming",
    version = "1.4.2.3",
    license = 'MIT',
    author = "Shono1",
    author_email = "shonor47@gmail.com",
    description = "Library for playing a standard game of checkers/draughts",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/Shono1/checkers",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)