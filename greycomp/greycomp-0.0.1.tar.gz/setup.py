import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="greycomp", # Replace with your own username
    version="0.0.1",
    author="Nishant Singh Hada",
    author_email="hadanis.sing@gmail.com",
    description="Greyscale Image Compression",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ThisIsNSH/Grey-Image-Compression",
    project_urls={
        "Bug Tracker": "https://github.com/ThisIsNSH/Grey-Image-Compression/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)