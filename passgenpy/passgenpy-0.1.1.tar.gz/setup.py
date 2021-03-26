from distutils.core import setup

setup(
  name = 'passgenpy',         # How you named your package folder (MyLib)
  packages = ['passgenpy'],   # Chose the same as "name"
  version = '0.1.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description='A password generator written in Python 3.x',   # Give a short description about your library
  author='Pavlos Efstathiou',                   # Type in your name
  author_email='paulefstathiou@gmail.com',      # Type in your E-Mail
  url='https://github.com/Pavlos-Efstathiou/Password-Generator/',
  download_url='https://github.com/Pavlos-Efstathiou/Password-Generator/archive/v_011.tar.gz', 
  keywords=['random', 'password', 'generator'],   # Keywords that define your package best
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
