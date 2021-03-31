import setuptools

long_description = """
# ttkbootstrap
A collection of modern flat themes inspired by Bootstrap. There are more than a dozen built-in themes, and you have the 
ability to easily create your own with TTK Creator.

## Installation
https://pypi.org/project/ttkbootstrap/
```python
pip install ttkbootstrap
```

## Usage
For more information about how to use this project in your own programs, please check out the 
[documentation](https://ttkbootstrap.readthedocs.io/en/latest/) on ReadTheDocs. You can find examples of all the themes 
as well as usage instructions.
"""

setuptools.setup(
    name="ttkbootstrap",
    version="0.0.17",
    author="Israel Dryer",
    author_email="israel.dryer@gmail.com",
    description="A collection of modern ttk themes inspired by Bootstrap",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/israel-dryer/ttkbootstrap",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    package_data={"": ["*.json"]},
    include_package_data=True,
    install_requires=["pillow"],
    python_requires=">=3.6",
)