from setuptools import setup, find_packages
import os

base_dir = os.path.dirname(__file__)
with open(os.path.join(base_dir, "README.md")) as f:
    long_description = f.read()

classifiers = [
    "Development Status :: 4 - Beta",
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='dprofiles',
    version="0.0.2",
    description='Discord Oauth2 Client for Quart and a easy to use API Wrapper for dprofiles.xyz',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Titanic-official/dprofiles',
    author='Titanic',
    author_email='admin@dprofiles.xyz',
    license='MIT LICENSE',
    classifiers=classifiers,
    keywords=['discord', 'Oauth2', 'discordpy',"discord py"],
    packages=["dprofiles","dprofiles.ext"],
    install_requires=['requests', 'quart', 'aiohttp','authlib']
)
