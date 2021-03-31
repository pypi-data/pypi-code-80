import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="teleimg",
  version="0.0.3",
  author="NotMe",
  author_email="eichitang@gmail.com",
  description="Help you upload a image to telegraph server,then get an url for this image.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)