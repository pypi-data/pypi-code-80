from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='randpercent',
  version='0.0.1',
  description='A library to generate booleans with a given percentage.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Eric Sivak',
  author_email='eric.sivak05@googlemail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='random, booleans', 
  packages=["randperc"],
  install_requires=[''] 
)
