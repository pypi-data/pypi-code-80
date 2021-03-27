from setuptools import setup

setup(name="gtodo",
      version='0.2',
      description='Simple note taking CLI app',
      long_description=open('README.md').read(),
      author='Samuel Ján Mucha',
      author_email='samueljanmucha1@gmail.com',
      license='MIT',
      py_modules=['main'],
      install_requires=['Click', ],
      entry_points='''
        [console_scripts]
        gtodo=main:gtodo
      ''')
