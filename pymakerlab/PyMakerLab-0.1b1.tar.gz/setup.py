import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyMakerLab",
    version="0.1.b1",
    author="AlexBroNikitin",
    author_email="alexnikitin071209@gmail.com",
    description="Python project managament, GUI Inteface, Cloud Functions and more!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://alexbronikitin.github.io/pymaker/",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=['pyrebase']
)
