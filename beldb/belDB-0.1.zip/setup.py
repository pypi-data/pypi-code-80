from distutils.core import setup
setup(
  name = 'belDB',
  packages = ['belDB'],  
  version = '0.1',      
  license='MIT',       
  description = 'A cool python package that makes the world of databases a lot easier.', 
  author = 'Itay Beladev',            
  author_email = 'itaybel2121@gmail.com', 
  url = 'https://github.com/Itay212121',  
  download_url = 'https://github.com/Itay212121/belDB/archive/refs/tags/0.1.tar.gz',  
  keywords = ['DataBase', 'db', 'easy', 'quick'],   # Keywords that define your package best
  install_requires=[],
  classifiers=[
    'Development Status :: 4 - Beta',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
