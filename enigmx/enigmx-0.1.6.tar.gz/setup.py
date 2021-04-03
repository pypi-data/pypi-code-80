import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'enigmx',      
  include_package_data = True,
  packages=setuptools.find_packages(),
  version = '0.1.6',    
  license='MIT',        
  description = 'enigmx package',   
  author = 'Quantmoon Technologies', 
  author_email = 'info@quantmoon.tech',
  url = 'https://www.quantmoon.tech',   
  install_requires=[        
          "pandas>=0.22.0",
          "numpy>=1.18.2",
          "zarr",
          "fracdiff==0.1.0",
          "ray",
          "numba",
          "pandas-market-calendars",
          "pyodbc",
          "xarray",
          "SQLAlchemy",
          "matplotlib",
          "tsfresh",
          "finnhub-python",
          "gcsfs",
          "imbalanced-learn==0.7.0"
      ],
  classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
  ],
  python_requires = ">=3.5",
)