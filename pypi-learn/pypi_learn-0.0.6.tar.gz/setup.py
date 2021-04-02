"""
to publish our package
"""
import os
from setuptools import setup


def read(filename):
    """
    reading README file
    """
    with open(os.path.join(os.path.dirname(__file__), filename)) as _in:
        return _in.read()


# This call to setup() does all the work
setup(
    name="pypi_learn",
    # The version of this library.
    # Read this as
    #   - MAJOR VERSION 1
    #   - MINOR VERSION 0
    #   - MAINTENANCE VERSION 0
    version="0.0.6",
    description="Generates a dataset for the Turkish speech recognition.",
    # description and Project name| library name
    long_description=read('README.md'),
    long_description_content_type="text/markdown",

    author="ARDIC R&D",
    author_email="yavuz.erzurumlu@ardictech.com",
    url="https://github.com/IoT-Ignite/pypi_learn",
    # These are the dependencies the library needs in order to run.
    install_requires=[
        'youtube-channel-transcript-api',
        'youtube_transcript_api',
        'youtube-dl',
        'launchpadlib',
    ],

    py_modules=["pypi_learn", "pypi_learn/crop_mp3_srt/crop_mp3_srt",
                "pypi_learn/youtube_srt_mp3",
                "pypi_learn/helper/helper"],
    packages=['pypi_learn'],
    packages_dir={'': 'pypi_learn'},

    include_package_data=True,

    entry_points={
        "console_scripts": [
            "pypi_learn=pypi_learn:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers"
    ],

    # Here are the keywords of my library.
    keywords='dataset, speech recognition, srt, youtube srt',
    license="MIT",
)
