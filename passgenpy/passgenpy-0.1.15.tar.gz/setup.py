from distutils.core import setup


with open("README.md", "r", encoding="utf-8") as fh:
    long_descript = fh.read()
setup(
  name = "passgenpy",
  packages = ["passgenpy"],
  version = "0.1.15",
  license="MIT",      
  description="A password generator written in Python 3.x",   # Give a short description about your library
  long_description=long_descript,
  # long_description_content_type="text/markdown",
  author="Pavlos Efstathiou",                 
  author_email="paulefstathiou@gmail.com",
  url="https://github.com/Pavlos-Efstathiou/Password-Generator/",
  download_url="https://github.com/Pavlos-Efstathiou/Password-Generator/archive/v_015.tar.gz", 
  keywords=["random", "password", "generator"], 
  # install_requires=[],
  classifiers=[
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Build Tools",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
  ],
)
