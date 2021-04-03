import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ordina-xml-csv-parser", # Replace with your own username
    version="0.0.2",
    author="Michael Groenewegen van der Weijden, Mihail Bondarenco, Rostislav Ivanov",
    author_email="",
    license='MIT',
    description="Parse puplic dvs data for ordina school project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/michael-gvdw/ordina-xml-csv-parser.git",
    project_urls={
        "Bug Tracker": "https://github.com/michael-gvdw/ordina-xml-csv-parser.git",
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "pandas==1.2.3",
        "numpy==1.20.1",
    ]
)