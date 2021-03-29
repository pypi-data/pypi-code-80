import sys
from os.path import abspath, dirname, join

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


PY3 = sys.version_info > (3,)

VERSION = None
version_file = join(dirname(abspath(__file__)), 'src', 'WebScreens', 'version.py')
with open(version_file) as file:
    code = compile(file.read(), version_file, 'exec')
    exec(code)

DESCRIPTION = """
Library to simulate different web screen resolutions using selenium library
"""[1:-1]

CLASSIFIERS = """
Operating System :: OS Independent
Programming Language :: Python
Topic :: Software Development :: Testing
"""[1:-1]


setup(
      name='robotframework-webscreens',
      version=VERSION,
      description='Library to simulate different web screen resolutions using selenium library',
      long_description=DESCRIPTION,
      author='Shiva Adirala',
      author_email='adiralashiva8@gmail.com',
      url='https://github.com/adiralashiva8/robotframework-webscreens',
      license='MIT',
      keywords='robotframework testing automation selenium web screen resolution',
      platforms='any',
      classifiers=CLASSIFIERS.splitlines(),
      package_dir={'': 'src'},
      packages=['WebScreens'],
      install_requires=[
          'robotframework',
          'robotframework-seleniumlibrary'
      ],)