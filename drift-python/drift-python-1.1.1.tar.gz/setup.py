from setuptools import setup
from drift import __version__


packages = ['drift']

requires = [
    'requests>=2.20.0'
]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='drift-python',
      version=__version__,
      description="A Simple Drift API Wrapper.",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Drift Engineering',
      author_email='driftintegrations@drift.com',
      packages=packages,
      url='https://github.com/Driftt/drift-python',
      include_package_data=True,
      zip_safe=False,
      license='MIT',
      install_requires=requires
)
