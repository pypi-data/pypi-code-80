import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dh0cker",
    version="0.1.5",
    author="dh0ck",
    author_email="dh0ck666@gmail.com",
    description="test package",
    long_description="Secrets were leaked in the previous version, now it's fixed",
    long_description_content_type="text/markdown",
    url="https://github.com/dh0ck/dh0cker",
    packages=setuptools.find_packages(),
    install_requires  = [], # List all your dependencies inside the list
    license = 'MIT'
)