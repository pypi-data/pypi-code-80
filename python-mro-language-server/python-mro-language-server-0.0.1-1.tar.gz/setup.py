from setuptools import setup
from os import path

DIR = path.dirname(path.abspath(__file__))
INSTALL_PACKAGES = open(path.join(DIR, 'requirements.txt')).read().splitlines()[1:]
TEST_PACKAGES = open(path.join(DIR, 'requirements-dev.txt')).read().splitlines()[1:]
TEST_PACKAGES = [pkg for pkg in TEST_PACKAGES if pkg not in INSTALL_PACKAGES]

with open(path.join(DIR, 'README.md')) as f:
    README = f.read()

setup(
    name='python-mro-language-server',
    packages=['mrols'],
    description="A simple Python language server to provide MRO (Method Resolution Order) inference via Hover and CodeLens.",
    long_description=README,
    long_description_content_type='text/markdown',
    install_requires=INSTALL_PACKAGES,
    version='0.0.1',
    url='https://github.com/mosckital/python-mro-language-server',
    author='Kaiyan XIAO',
    author_email='k.max.xiao@gmail.com',
    keywords=['MRO', 'language-server', 'method-resolution-order', 'syntax-analysis'],
    tests_require=TEST_PACKAGES,
    python_requires='>=3.6',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
    ],
)