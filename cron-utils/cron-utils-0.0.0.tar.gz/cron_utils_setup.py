"""Setup for the cron-utils package."""

import setuptools


with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Rahul Kumar",
    author_email="rahul@trell.in",
    name='cron-utils',
    description='Utility code for cron alerting and monitoring',
    version='v0.0.0',
    long_description=README,
    url='https://https://gitlab.com/trell/cron-utils/',
    packages=setuptools.find_packages(),
    python_requires=">=3.6.9",
    install_requires=['requests', 'psutil',
                      ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'

    ],
)


