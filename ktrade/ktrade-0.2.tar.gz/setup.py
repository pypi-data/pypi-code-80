import pathlib
import re

import setuptools


root_dir = pathlib.Path(__file__).parent

description = 'KrossTrading Core Package'

long_description = 'KrossTrading core package for multi-vendor, clients'
#long_description = (root_dir / 'README.md').read_text(encoding='utf-8')

# PyPI disables the "raw" directive.
#long_description = re.sub(
#    r"^\.\. raw:: html.*?^(?=\w)",
#    "",
#    long_description,
#    flags=re.DOTALL | re.MULTILINE,
#)

exec((root_dir / 'ktrade' / 'version.py').read_text(encoding='utf-8'))

packages = ['ktrade', 'ktrade/protocol', 'ktrade/stock']

setuptools.setup(
    name='ktrade',
    version=version,
    description=description,
    long_description=long_description,
    url='https://github.com/krosstrading/ktrade',
    author='KrossTrading',
    author_email='contacts@krosstrading.com',
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    package_dir = {'': '.'},
    #package_data
    packages=packages,
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.7',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    #test_loader='pytest',
)

