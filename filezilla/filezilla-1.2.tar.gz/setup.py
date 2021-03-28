from setuptools import setup, find_packages
import pathlib
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
setup(
    name = 'filezilla',
    version = '1.2',
    scripts = ['./script/filezilla'],
    author = 'Gaurav Arora',
    description = ('File manager'),
    long_description = README,
    long_description_content_type = "text/markdown",
    packages = ['filezilla'],
    install_requires=[
        'setuptools',
        'PyPDF2 >= 1.26.0',
        'Pillow >= 7.0.0'
    ],
    python_requires='>=3.7'
)