import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
long_description = (HERE / "README.md").read_text()

setup(
    name='calculation_cells',
    packages=['cell'],
    description='Library for calculate through formula and variables',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.1',
    url='https://github.com/dmalisani/calculation_cells',
    author='Daniel Malisani',
    author_email='dmalisani@gmail.com',
    keywords=['calculation','formula','variable'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    include_package_data=False,
    )
