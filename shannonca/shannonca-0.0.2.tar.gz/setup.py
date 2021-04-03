from distutils.core import setup
setup(
  name = 'shannonca', 
  packages = ['shannonca'],  
  version = '0.0.2',   
  license='MIT',       
  description = 'Informative Dimensionality Reduction via Shannon Component Analysis',   
  author = 'Benjamin DeMeo',                   
  author_email = 'bdemeo@g.harvard.edu',      
  url = 'https://github.com/bdemeo/shannonca',  
  download_url =  'https://github.com/bendemeo/shannonca/archive/refs/tags/0.0.1.tar.gz',
  keywords = ['Shannon', 'Information', 'Dimensionality','reduction', 'single-cell','RNA'], 
  install_requires=[           
          'sklearn',
          'scipy',
          'numpy',
          'matplotlib',
          'pandas',
          'seaborn',
          'scanpy'
      ]
    )
