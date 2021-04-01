import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="platemapping", 
    version="2.0.0",
    author="Stuart Warriner, Lawrence Collins, Mariusz Las",
    author_email="s.l.warriner@leeds.ac.uk, lawrencejordancollins@gmail.com, cm18mel@leeds.ac.uk",
    description="Plate map uploading, processing & visualisaion",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lawrencecollins/platemapping",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    setup_requires=['wheel']
)
