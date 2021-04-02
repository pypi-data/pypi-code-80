import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="csv_upload", 
    version="0.0.1",
    author="Om Kumar Sahu",
    author_email="omkumarsahu.26@gmail.com",
    description="This app updates the database with csv upload",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/omkumar01/csv_upload",
    project_urls={
        "Bug Tracker": "https://github.com/omkumar01/csv_upload/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)