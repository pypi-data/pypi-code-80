from setuptools import setup
from setuptools import find_packages


setup(name='PSM_testbed',
      version='0.0.0.13',
      description='A testbed package for Phillip Maire',
      packages=find_packages(),
      author_email='phillip.maire@gmail.com',
      zip_safe=False,
      install_requires=[
       "natsort==7.1.1",
       "pyicu",])

#      packages=['PSM_testbed'],
