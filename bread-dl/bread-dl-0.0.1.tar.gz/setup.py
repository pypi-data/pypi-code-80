from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))
setup(
    name='bread-dl',
    version='0.0.1',
    description='Basic processing tools in common algorithms.',
    url='https://github.com/Joe-Laue/bread-dl',

    # Author details
    author='Joe',
    author_email='joe.laue@outlook.com',

    # Packages
    packages=['bread.dl',
              'bread.dl.utils',
              'bread.dl.layers'],

    # License
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    py_modules=["bread-dl"]
)
