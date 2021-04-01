from setuptools import setup
import pathlib

README = (pathlib.Path(__file__).parent / "README.md").read_text()

setup(
    name="anonfiles-py",
    version="0.1.1",
    description="Simple AnonFiles.com API Wrapper",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/TheBoringDude/anonfiles.py",
    author="TheBoringDude",
    author_email="iamcoderx@gmail.com",
    license="MIT",
    project_urls={
        "Bug Tracker": "https://github.com/TheBoringDude/anonfiles.py/issues"
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["anonfiles"],
    include_package_data=True,
    install_requires=["requests"],
)