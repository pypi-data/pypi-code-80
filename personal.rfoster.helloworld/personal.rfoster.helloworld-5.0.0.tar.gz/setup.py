import os
from setuptools import setup, find_packages

def read(fname):
  return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
  name = "personal.rfoster.helloworld",
  version = "5.0.0",
  author = "Rod Foster",
  author_email = "rod_foster@intuit.com",
  url = "https://github.intuit.com/dev-patterns/docker-oicp-alpine",
  license = "GPLv3",
  description = "Helloworld App to Test Alpine Images",
  packages = ["helloworld"],
  package_dir = {"rfoster": "helloworld"},
  install_requires = ["flask"],

  # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
  classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "License :: Other/Proprietary License",
    "Operating System :: POSIX :: Other",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.7"
  ]
)
