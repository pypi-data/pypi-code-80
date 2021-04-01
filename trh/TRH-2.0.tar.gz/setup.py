from setuptools import setup, find_packages
import os



VERSION = '2.0'
DESCRIPTION = 'TypeRacer and MonkeyType Hack using Selenium Chromium Webdriver and BeatifulSoup Web Scraping.'

# Setting up
setup(
    name="TRH",
    version=VERSION,
    author="TanmayArya1-p",
    author_email="<tanmayarya2018@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['selenium', 'beautifulsoup4'],
    keywords=['python', 'selenium', 'web-scraping'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)