from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Test Package'
LONG_DESCRIPTION = 'A Test Package on Census Data API.'

# Setting up
setup(
    name="TestSum",
    version=VERSION,
    author="Salah Uddin Momtaz",
    author_email="<sm1335@jagmail.southalabama.edu>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['Test', 'Python', 'Sum'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)