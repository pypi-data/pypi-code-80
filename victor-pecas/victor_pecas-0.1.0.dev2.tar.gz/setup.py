from victor_pecas import __version__

from collections import OrderedDict

import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="victor_pecas",
    version=f"{__version__}",
    author="GPAM",
    author_email="gpam@gmail.com",
    description="GPAM Victor Pecas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache-2.0",
    url="https://gitlab.com/gpam/victor/SERVICES/victor-pecas",
    packages=setuptools.find_packages(include=["victor_pecas", "victor_pecas.*"]),
    python_requires=">=3.6.0",
    project_urls=OrderedDict(
        (
            ("Documentation", "https://gitlab.com/gpam/victor/SERVICES/victor-pecas"),
            ("Code", "https://gitlab.com/gpam/victor/SERVICES/victor-pecas"),
            ("Issue tracker", "https://gitlab.com/victor/SERVICES/victor-pecas/issues"),
        )
    ),
    install_requires=["nltk>=3.4.5", "numpy>=1.18.3", "scikit_learn>=0.22.2.post1"],
    tests_require=[
        "pytest",
        "flake8",
        "pytest-cov",
        "pytest-mock",
        "isort",
        "black",
    ],
    setup_requires=["setuptools>=38.6.0"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries",
    ],
)
