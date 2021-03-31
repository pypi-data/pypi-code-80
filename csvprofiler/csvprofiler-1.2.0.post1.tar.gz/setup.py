#!python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="csvprofiler",
    version="1.2.0-1",
    author="Larry Kuhn",
    author_email="LarryKuhn@outlook.com",
    description="An extensible CSV column profiling and validation utility",
    keywords="validation etl analytics batch profile regular-expressions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LarryKuhn/CSV-Profiler",
    packages=setuptools.find_packages(),
    scripts=["csvpcg.py", "csvprofiler.py", "wrapdemo.py", "profmod.py"],
#    entry_points={
#        'console_scripts': [
#            'csvpcg = csvpcg:main',
#            'csvprofiler = csvprofiler:main'
#        ]
#    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        "Topic :: Office/Business",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        "Topic :: Text Processing",
        "Topic :: Utilities"
    ],
    install_requires=['pandas>=1.1.5'],
    python_requires='>=3.6',
)