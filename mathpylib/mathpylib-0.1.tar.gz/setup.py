from setuptools import setup
setup(
    name='mathpylib',version='0.1',description='A Python Library to do math functions.',author='Pranav',license='MIT',entry_points={
        'console_scripts':['mathpylib=mathpylib.interp:main']
    },install_requires=['virtualenv','wheel','setuptools','pip','HCF'],packages=['mathpylib']
)