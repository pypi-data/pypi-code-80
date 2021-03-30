from setuptools import find_packages, setup


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
  name = 'pypijhjoh',          
  version = '0.3.4',      
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository 
  author = 'Joakim Johansen',
  description="Test package by jhjoh",
  long_description=long_description,
  long_description_content_type="text/markdown",                   
  author_email = 'jhjoh@equinor.com',         
  keywords = ['TEST', 'PYPI'],   
  install_requires=[            
          'numpy',
  ],
  classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
  ],
  packages=find_packages(),
  python_requires=">=3.6",
)