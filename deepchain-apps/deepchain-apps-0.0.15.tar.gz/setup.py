import pathlib
from subprocess import check_call
from typing import List

from setuptools import find_packages, setup
from setuptools.command.install import install

from deepchainapps.version import VERSION

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()


req = [
    "numpy>=1.16",
    "requests>=2.23.0",
    "torch==1.5.0",
    "tensorflow==2.2.0",
    "fair-esm==0.3.1",
]


def make_install():

    setup_fn = setup(
        name="deepchain-apps",
        version=VERSION,
        description="Define a personnal scorer for the user of DeepChain.bio",
        author="Instadeep",
        long_description=README,
        long_description_content_type="text/markdown",
        author_email="a.delfosse@instadeep.com",
        packages=find_packages(),
        entry_points={
            "console_scripts": ["deepchain=deepchainapps.cli.deepchain:main"],
        },
        install_requires=req,
        include_package_data=True,
        zip_safe=False,
        python_requires=">=3.7",
    )

    return setup_fn


if __name__ == "__main__":
    make_install()
