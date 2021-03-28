from setuptools import setup

setup(name='metro_cost',
      version='0.1',
      description='A model that can predict the cost of metro construction',
      url='http://github.com/storborg/metro_cost',
      author='Manolo',
      author_email='manolo@example.com',
      license='MIT',
      packages=['metro_cost'],
      install_requires=[
            'pandas',
            'numpy',
            'matplotlib',
            'sklearn',
            'catboost',
            'lightgbm'
      ],
      zip_safe=False)