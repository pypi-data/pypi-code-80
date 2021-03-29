from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    author='Aderemi Adesada',
    author_email='adesadaaderemi@gmail.com',
    name='genesys',
    version='0.0.2',
    description='generates files and dependences for cgi projects',
    packages=['genesis'],
    package_dir={'': '.'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent"
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires = [
        "flask==1.1.2",
        "flask-restful==0.3.8"
    ]
)