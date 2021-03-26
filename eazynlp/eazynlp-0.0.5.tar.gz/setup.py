import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="eazynlp",
    version="0.0.5",
    author="Info CodeBrew",
    author_email="info.codebrew@gmail.com",
    description="NLP made easy for researchers",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/tumeri/eazynlp",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    install_requires=["matplotlib", "nltk", "pandas", "wordcloud"],
    python_requires='>=3.6'
)
