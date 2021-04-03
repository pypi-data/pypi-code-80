import os
import sys
from setuptools import find_packages, setup
def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()
def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            # __version__ = "0.9"
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")
setup(
    name="pynim",
    version=get_version("src/pynim/__init__.py"),
    description="pynim - a tool for build instaler for Python scripts.",
    classifiers=[
        'Intended Audience :: Developers',
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Microsoft :: Windows :: Windows XP",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Operating System :: Microsoft :: Windows :: Windows 8",
        "Operating System :: Microsoft :: Windows :: Windows 8.1",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    keywords='python nsis installer maker exe build builder pyinstaller',
    author='AmirAli Mollaie',
    package_dir={"": "src"},
    package_data={'': ['src/pynim/installer.nsi',]},
    include_package_data=True,
    packages=find_packages(where="src"),
    entry_points={"console_scripts": ["pynim=pynim.__init__:main",]},
    install_requires=['pyinstaller','argparse'],
    zip_safe=True,
    long_description=read("README.md"),
    python_requires='>=3.6',
)
