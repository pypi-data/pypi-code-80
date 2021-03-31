from codecs import open
import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), 'r') as infile:
    long_description = infile.read()

about = {}
with open(os.path.join(here, 'hyperkv', '__version__.py'), 'r', encoding='utf-8') as infile:
    exec(infile.read(), about)

setup(
    name='hyperkv',
    version=about['__version__'],
    packages=[
        'hyperkv',
    ],
    entry_points={
        'console_scripts': [
            'hyperkv = hyperkv.cli:command_line',
        ],
    },
    url='https://github.com/phistrom/hyperkv',
    license='MIT',
    author='Phillip Stromberg',
    author_email='phillip@strombergs.com',
    description='Reads from Hyper-V KV on a Linux guest',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ),
    zip_safe=False,
    long_description=long_description,
    long_description_content_type="text/markdown",
)
