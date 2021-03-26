# you can name anything this file
# but i am sticking with setup.py as my filename

from setuptools import find_packages, setup

VERSION = '0.0.2'
DESCRIPTION = "This is my first package that will be uploaded on pip"
LONG_DESCRIPTION = "This is just a long description "

### setting up out package ###
setup(
    name = 'mainmodule', ## note it should match with your package folder name
    version = VERSION,
    author = 'amit',
    author_email = "fulldev101@gmail.com",
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    packages = find_packages(),
    install_requires = ['requests','numpy'], ## let's say we need numpy and requests
    keywords = ['amit','amit-package-tutorial','tutorial'], ## keywords to search your package
    classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]


)
