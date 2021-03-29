from setuptools import setup, find_packages
from io import open
from os import path

# The directory containing this file
here = path.abspath(path.dirname(__file__))

# automatically captured required modules for install_requires in requirements.txt and as well as configure dependency links
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')
install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (
    not x.startswith('#')) and (not x.startswith('-'))]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs \
                    if 'git+' not in x]
with open("README.md", "r") as fh:
    long_description = fh.read()

print("PACKAGES: {}".format(find_packages()))

setup (
    name = 'dd_jinja_renderer',
    description = 'A command line tool to generate jinja templates',
    version = '1.0.4',
    packages = find_packages(), # list of all packages
    install_requires = install_requires,
    python_requires='>=3.4', # any python greater than 3.4
    entry_points={
        'console_scripts': [
            'jinja-renderer=jinja_renderer.__main__:main',
        ],
    },
    author="Calle Holst",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    url='https://bitbucket.org/dataductus/jinja-renderer',
    download_url='https://bitbucket.org/dataductus/jinja-renderer/1.0.0.tar.gz',
    dependency_links=dependency_links,
    author_email='dummy@dataductus.se',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ]
)
