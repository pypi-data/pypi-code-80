import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='easy_to_cython',
    version='1.0.0',
    packages=setuptools.find_packages(),
    url='https://github.com/pypa/sampleproject',
    license='MIT',
    author='Elijah',
    author_email='610152942@qq.com',
    description='Simple and easy to packages code replace cython',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['Cython'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'easy-to-cython-build=easy_to_cython.build:build',
            'easy-to-cython-package=easy_to_cython.action:package',
            'easy-to-cython-release=easy_to_cython.action:release'
        ]
    },
)
