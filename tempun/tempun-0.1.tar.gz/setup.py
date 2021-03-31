import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tempun", # Replace with your own username
    version="0.1",
    author="Vojtech Kase",
    author_email="vojtech.kase@gmail.com",
    description="A package to deal with temporal uncertainty in historical/archaeological datasets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sdam-au/sddk",
    packages=setuptools.find_packages(),
    install_requires=[
        "pandas>=1",
        "numpy",
        "scipy>=1.5",
        "matplotlib>=3.4"
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)
