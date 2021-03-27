from setuptools import setup


with open('README.md', 'r') as f:
    read= f.read()


setup(
    name='ImageLayers',
    version='0.4.2',
    packages=['imagelayers'],
    install_requires=['pillow'],
    description='Split and process image segments and layers.',
    long_description=read,
    long_description_content_type='text/markdown',
    url='https://github.com/GrandMoff100/ImageLayers',
    author='GrandMoff100',
    author_email='nlarsen23.student@gmail.com'
)