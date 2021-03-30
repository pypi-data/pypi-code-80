import os
import setuptools

VERSION = "0.8"
with open(os.path.join(os.path.dirname(__file__), "README.md"), "r") as r:
    README = r.read()

setuptools.setup(
    name='fuid',
    version=VERSION,
    description='Fast, scalable unique ID generation',
    long_description=README,
    long_description_content_type='text/markdown',
    url='http://github.com/husseinraed/fuid.py',
    py_modules=['fuid'],
    author='Hussein Raed',
    author_email='me@husseinraed.cf',
    install_requires=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
