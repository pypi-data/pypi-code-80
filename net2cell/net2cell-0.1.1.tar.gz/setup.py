import setuptools

setuptools.setup(
    name='net2cell',
    version='0.1.1',
    author='Jiawei Lu, Xuesong Zhou',
    author_email='jiaweil9@asu.edu, xzhou74@asu.edu',
    url='https://github.com/jiawei92/net2cell',
    description='automatically build hybrid transportation networks',
    long_description=open('README_pypi.rst').read(),
    license='GPLv3+',
    packages=['net2cell'],
    install_requires=['pandas >= 0.24.0'],
    classifiers=['License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                 'Programming Language :: Python :: 3']
)
