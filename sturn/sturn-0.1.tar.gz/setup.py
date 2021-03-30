from distutils.core import setup
setup(
  name = 'sturn',         
  packages = ['sturn'],   
  version = '0.1',      
  license='MIT',        
  description = 'A simple desktop rotating python module',
  author = 'Advaith S',                  
  author_email = 'professionaladu@hotmail.com',      
  url = 'https://github.com/Beatz-22/sTurn',   
  download_url = 'https://github.com/Beatz-22/sTurn/archive/refs/tags/v_0.1.tar.gz', 
  keywords = ['rotate', 'useful', 'screen-rotate'], 
  install_requires=[           
          'pyautogui'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License', 
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)