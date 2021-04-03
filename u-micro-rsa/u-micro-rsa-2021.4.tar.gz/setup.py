from setuptools import setup, find_packages

DESCRIPTION = "A pure python implementation of the RSA encryption algorithm"

setup(
    name="u-micro-rsa",
    version="2021.4",
    license="GNU General Public License Version 3.0",
    author="Z-40",
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    url="https://github.com/Z-40/MicroRSA",
    install_requires=[],
    keywords=[
        "python", 
        "RSA", 
        "encryption", 
        "public-key-cryptography"
    ],
    packages=["micro_rsa"],
    package_data={
        "micro_rsa": [
            "doc/CHANGELOG.md", 
            "doc/LICENSE.txt",
            "doc/README.md",
        ]
    },
    include_package_data=True
)
