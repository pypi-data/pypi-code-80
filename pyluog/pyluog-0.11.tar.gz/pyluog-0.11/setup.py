from setuptools import setup,find_packages

setup(name='pyluog',
      version='0.11',
      description='A python module for using Luogu Api.',
      url='',
      author='hlwdy',
      author_email='hlwdyck@gmail.com',
      license='MIT',
      packages=find_packages('src', exclude=['requests','matplotlib','PIL']),
      python_requires=">=3.6",
)