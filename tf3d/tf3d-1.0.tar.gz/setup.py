from setuptools import setup, find_packages, Extension
from os import path

__version__ = '1.0'


# Add Native Extensions
# See https://docs.python.org/3/extending/building.html on details
ext_modules = []
#ext_modules.append(Extension('demo', sources = ['demo.c']))

# Parse requirements.txt
with open(path.join(path.abspath(path.dirname(__file__)), 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')
install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')]

# Call the setup.py
setup(
    name='tf3d',
    version=__version__,
    author='Michael Fuerst',
    author_email='mail@michaelfuerst.de',
    license='MIT',
    packages=find_packages(exclude=['docs', 'images', 'tests', 'examples']),
    # Alternative if you prefer to have a package as a subfolder of src, instead of subfolder of root.
    # package_dir={'': 'src'},
    # packages=find_packages(where='src'),
    install_requires=install_requires,
    dependency_links=dependency_links,
    ext_modules=ext_modules,
    extras_require={
        'dev': ['nose2', 'packaging'],
    },
)
