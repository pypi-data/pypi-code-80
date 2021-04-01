import setuptools

with open("README.md", "r") as fh: long_description = fh.read()

setuptools.setup(
    name="my-FIRSt-pkg-name", 
    version="0.0.1", 
    author="Example Author", 
    author_email="author@example.com", 
    description="A small example package", 
    long_description=long_description, 
    long_description_content_type="text/markdown", 
    url="https://github.com/pypa/sampleproject", 
    packages=setuptools.find_packages(exclude=["期望发布的包"]), 
    classifiers=[ "Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License", "Operating System :: OS Independent", ], 
    python_requires='>=3.6',
)
