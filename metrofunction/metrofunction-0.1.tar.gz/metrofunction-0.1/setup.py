from setuptools import setup

setup(name='metrofunction',
      version='0.1',
      description='A function that can predict the cost of metro construction',
      url='http://github.com/storborg/metrofunction',
      author='Manolo',
      author_email='manolo@example.com',
      license='MIT',
      packages=['metrofunction'],
      install_requires=[
            'pandas',
            'numpy',
            'matplotlib',
            'sklearn',
            'shap',
            'statsmodels',
            'catboost',
            'lightgbm'
      ],
      zip_safe=False)