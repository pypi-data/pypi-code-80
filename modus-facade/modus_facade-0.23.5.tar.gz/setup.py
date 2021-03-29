"""Establish Setup and Install requirements for the Facade package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='modus_facade',
    version='0.23.5',
    description='Modus Facade',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/dotmodus/facade',
    author='DotModus',
    author_email='developers@dotmodus.com',
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=[
        'google-api-python-client~=1.12.8',
        'google-cloud-storage~=1.36.1',
        'google-cloud-bigquery~=2.10.0',
        'oauth2client~=4.1.3',
        'humanize',
        'requests',
        'simplejson',
        'pytz'
    ],
    extras_require={
        'dev': [
            'unittest2',
            'vcrpy',
            'pytest',
            'coverage',
            'codacy-coverage',
            'requests-mock',
            'psutil',
        ],
        'mod_redis': [
            'redis'
        ]
    },
    zip_safe=False
)
