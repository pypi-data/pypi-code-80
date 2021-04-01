#!/usr/bin/env python
# -*- encoding: utf-8 -*-


from glob import glob
from os.path import basename
from os.path import splitext
from pathlib import Path
from typing import List
from typing import Union

from setuptools import find_packages, setup


def parse_requirements(filename: Union[str, Path]) -> List:
    """Read requirements file in the style as produced by pip freeze.

    Parameters
    ----------
    filename : str or Path

    Returns
    -------
    list of required pkgs w/ evtl. version specs
    """
    with open(filename, "r", encoding="utf8") as f:
        lineiter = (line.strip() for line in f.readlines())
    return [line for line in lineiter if line and not line.startswith("#")]


DIR = Path(__file__).parent

README = (DIR / "README.md").read_text()
install_reqs = parse_requirements(DIR / "pip_requirements.txt")
dev_reqs = parse_requirements(DIR / "pip_requirements_dev.txt")

if __name__ == "__main__":
    setup(
        name="abox",
        version="0.0.0",
        author="abox-team",
        description="WIP",
        long_description=README,
        long_description_content_type="text/markdown",
        license="see file",
        license_files=('LICENSE',),
        packages=find_packages("src"),
        package_dir={"": "src"},
        py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
        zip_safe=False,
        classifiers=[
            "Development Status :: 1 - Planning",
            "Intended Audience :: Developers",
            "Operating System :: Unix",
            "Operating System :: POSIX",
            "Operating System :: Microsoft :: Windows",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Topic :: Utilities",
        ],
        python_requires=">=3.6",
        install_requires=install_reqs,
        extras_require={"dev": dev_reqs},
        entry_points={"console_scripts": []},
    )
