import os
from setuptools import setup, find_packages

def read(fname):
  return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
  name = "personal.koder.helloworld",
  version = "9.0.0",
  author = "tevkoder",
  author_email = "koder@tevora.com",
  license = "GPLv3",
  description = "Helloworld App DONTUSE for POC",
  packages = ["helloworld"],
  package_dir = {"tevkoder": "helloworld"},
  install_requires = ["flask"],

  # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
  classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Operating System :: POSIX :: Other",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.7"
  ]
)
