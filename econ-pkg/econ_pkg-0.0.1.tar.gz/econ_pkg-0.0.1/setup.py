import setuptools
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
    Extension('econ',
              ['pkg/econ.pyx','pkg/sample.cpp','pkg/sample1.cpp'],
              # Note here that the C++ language was specified
              # The default language is C
              language="c++",
              include_dirs = ["pkg", "sample.h"],
              #libraries=['trisha'],
              #library_dirs=['pkg/'])
    )]

setup(
    name = 'econ_pkg',
    version='0.0.1',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules,
    packages = setuptools.find_packages(),
    classifiers=[
    "License :: OSI Approved :: MIT License",   # Again, pick a license
    "Programming Language :: Python :: 3",      #Specify which pyhton versions that you want to support
    "Operating System :: OS Independent",
],
python_requires='>=3.6',
    # include_dirs=[np.get_include()]  # This gets all the required Numpy core files
)
