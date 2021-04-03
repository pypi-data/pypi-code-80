from setuptools import setup

setup(
    name='rlutils-python',
    version='0.0.1',
    packages=['rlutils'],
    url='https://github.com/vermouth1992/rlutils',
    license='Apache 2.0',
    author='Chi Zhang',
    author_email='czhangseu@gmail.com',
    description='Reinforcement Learning Utilities',
    entry_points={
        'console_scripts': [
            'rlplot=rlutils.plot:main',
            'rlrun=rlutils.run:main'
        ]
    }
)
