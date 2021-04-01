from setuptools import setup

setup(name='uofsc_calculus_labs',
      version='0.1',
      description='Functions for UofSC Calculus Labs',
      packages=['uofsc_calculus_labs'],
      author_email='cwarnock@math.sc.edu',
      zip_safe=False,
      setup_requires   = ['sage-package'],
     install_requires = ['sage-package', 'sphinx'])
