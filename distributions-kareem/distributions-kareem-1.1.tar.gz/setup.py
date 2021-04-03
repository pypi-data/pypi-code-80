from setuptools import setup

# Open local README file and read contents
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='distributions-kareem',
      version='1.1',
      packages=['distributions'],
      author= 'Kareem Ayyad',
      author_email = 'kareem@ayyad.net',
      description="A small package built for the Data Science Nanodegree program of Udacity for Gaussian and Binomial Distributions",
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False)