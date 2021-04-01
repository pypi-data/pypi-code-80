"""
Setup Module for LSST JupyterLab Utilities
"""
import codecs
import io
import os
import setuptools


def get_version(file, name="__version__"):
    """Get the version of the package from the given file by
    executing it and extracting the given `name`.
    """
    path = os.path.realpath(file)
    version_ns = {}
    with io.open(path, encoding="utf8") as f:
        exec(f.read(), {}, version_ns)
    return version_ns[name]


def local_read(filename):
    """Convenience function for includes"""
    full_filename = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), filename
    )
    return codecs.open(full_filename, "r", "utf-8").read()


NAME = "rubin_jupyter_utils.lab"
_path = NAME.replace('.', '/')
DESCRIPTION = "Utilities for Rubin Science Platform notebook aspect"
LONG_DESCRIPTION = local_read("README.md")
VERSION = get_version("{}/_version.py".format(_path))
AUTHOR = "Adam Thornton"
AUTHOR_EMAIL = "athornton@lsst.org"
URL = "https://github.com/sqre-lsst/rubin-jupyter-lab"
LICENSE = "MIT"

setuptools.setup(
    name=NAME,
    version=VERSION,
    long_description=LONG_DESCRIPTION,
    packages=setuptools.find_namespace_packages(
        include=["rubin_jupyter_utils.*"]),
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="lsst",
    install_requires=[
        "bokeh>=2,<3",
        "kubernetes>=11,<12",
        "maproxy>=0.0.12,<1",
        "pyvo>=1,<2",
        "nbreport>=0.7,<1.0",
        "requests>=2.22,<3.0",
        "jupyterhub>=1,<2",
        "jupyterlab>=2.2,<3.0",
        "semver>=2,<3",
        "rubin_jupyter_utils.helpers>=0.30.1,<1.0",
        "rubin_jupyter_utils.config>=0.30.2,<1.0"
    ],
    entry_points={
        'console_scripts': [
            'jupyter-labhub = ' + NAME + '.rubinlapapp.labhubapp:main',
            'jupyter-rubinlab = ' + NAME + '.rubinlabapp.rubinlabapp:main'
        ],
    },
    zip_safe=False,
)
