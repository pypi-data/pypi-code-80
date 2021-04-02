import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="tykit",
  version="0.0.1",
  author="tyyuan",
  author_email="1374736649@qq.com",
  description="A tool kit of progress bars and console logs with rich output",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/paperplane110/tykit.git",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)