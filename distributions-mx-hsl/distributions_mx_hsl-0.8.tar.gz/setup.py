from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="distributions_mx_hsl", 
    version="0.8",
    author="mx-hsl",
    description="Gaussian & Binomial distributions",
    packages=['distributions_mx_hsl'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License"
    ]
)