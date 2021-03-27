from setuptools import setup, find_packages
import os
import sys
import versioneer


# https://www.pydanny.com/python-dot-py-tricks.html
if sys.argv[-1] == 'test':

    r = os.system('pytest test -v && '
                  'xenon -b A -m A -a A -e "csirtgsdk/_version*" csirtgsdk')
    if r == 0:
        raise SystemExit

    raise RuntimeError('tests failed')

setup(
    name="csirtgsdk",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="CSIRTG Python SDK",
    long_description="CSIRTG Software Development Kit for Python",
    url="https://github.com/csirtgadgets/csirtgsdk-v2-py",
    license='MPL2',
    classifiers=[
        "Topic :: System :: Networking",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Programming Language :: Python"
    ],
    keywords=['network', 'security'],
    author="Wes Young",
    author_email="wes@csirtgadgets.com",
    packages=find_packages(exclude=['test']),
    install_requires=[
        'requests',
        'cachetools'
    ],
    entry_points={
        'console_scripts': [
            "csirtg=csirtgsdk.cli:get",
            'csirtg-create=csirtgsdk.cli:create'
        ]
    },
)
