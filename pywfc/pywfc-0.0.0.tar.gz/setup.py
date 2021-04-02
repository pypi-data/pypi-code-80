import setuptools


setuptools.setup(
    name="pywfc",
    version="0.0.0",
    url="https://github.com/FoxNerdSaysMoo/PyWFC",
    author="TeamNightSky",
    author_email="teamnightsky.gh@gmail.com",
    description="Python3 Wave Function Collapse Algorithm implementation",
    long_description=open("README.md", 'r').read(),
    long_description_content_type="text/markdown",
    packages=["wfc"],
    python_requires=">=3.6",
    classifiers=[
        "Operating System :: OS Independent"
    ]
)
