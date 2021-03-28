from setuptools import setup
import os
import codecs

# get the long description from the relevant file
here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="dragontide",
    version="1.0.0",
    description=("CCR extension to Dragonfly"),
    long_description=long_description,
    url="https://github.com/dsw88/dragontide",
    author="David Woodruff",
    author_email="themaplewoods@outlook.com",
    license="Unilicense",
    keywords="continuous command recognition, speech recognition, voice coding, dragonfly, Dragon",
    packages=["dragontide"],
    install_requires=["dragonfly2>=0.30.0"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: Public Domain",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Adaptive Technologies",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
