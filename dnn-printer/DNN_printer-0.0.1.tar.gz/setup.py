from setuptools import setup, Extension
import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='DNN_printer',
    version='0.0.1',
    author='CPing',
    author_email='635897373@qq.com',
    url='',
    description=u'Print feature map and weight size of PyTorch models.',
    long_description_content_type="text/markdown",
    long_description = long_description,
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[],
    entry_points={
        'console_scripts': [
        ]
    }
)
