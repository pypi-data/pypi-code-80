from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="sasconnect",
    version="3.0",
    description="Python SDK for API users",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://zebull.in",
    author="Pradeep",
    author_email="pradeep@stoneagesolutions.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Intended Audience :: Developers",
    ],
    packages=["sasconnect"],
    include_package_data=True,
    install_requires=["requests"],
)