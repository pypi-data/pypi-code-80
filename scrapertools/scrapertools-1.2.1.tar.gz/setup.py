from setuptools import setup

setup(
    name="scrapertools",
    version="1.2.1",
    packages=["scrapertools"],
    url="https://github.com/ultrafunkamsterdam/scrapertools",
    license="GPL3.0 License",
    author="ultrafunkamsterdam",
    author_email="info@ultrafunk.nl",
    description="scraping for humans",
    install_requires=[
        "requests",
    ],
    extras_require={
        "video": ["m3u8"]
    },
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
