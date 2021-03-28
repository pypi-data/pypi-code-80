from setuptools import setup, find_packages
setup(
    name='recache',
    version='1.0.0',
    description='Cache functions to speed up recursion',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/donno2048/recache',
    packages=find_packages(),
    license='MIT',
    author='Elisha Hollander',
    classifiers=['Programming Language :: Python :: 3']
)
