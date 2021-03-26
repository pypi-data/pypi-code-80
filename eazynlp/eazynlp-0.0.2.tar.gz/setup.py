import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eazynlp",
    version="0.0.2",
    author="Info CodeBrew",
    author_email="info.codebrew@gmail.com",
    description="NLP made easy for researchers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tumeri/eazynlp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)