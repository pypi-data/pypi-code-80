import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="leapdna",
    version="0.1.0",
    author="Elias Hernandis",
    author_email="elias@hernandis.me",
    description="A Python 3.9 implementation of the leapdna toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/knifecake/leapdna-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    include_package_data=True)
