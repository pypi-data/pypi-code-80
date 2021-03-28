from setuptools import setup, find_packages

setup(name="hola_paq",
      version="0.0.1",
      author="Miguel López Cruz",
      author_email="miguellcl@hotmail.com",
      url="",
      description="Another hello-world example package",
      py_modules=["hola"],
      package_dir={'': 'source'},
      packages=find_packages(),
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          ],
      )
      
