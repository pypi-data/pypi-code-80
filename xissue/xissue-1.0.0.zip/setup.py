
# from distutils.core import setup
from setuptools import  setup  #推荐使用

def readme_file():
      with open("README.rst", encoding="utf-8") as rf:
            return rf.read()

setup(name="xissue",
      version="1.0.0",
      description="this is a tools lirary.",
      packages=["xissue"],
      py_modules=["XTool"],
      author="ivey",
      author_email="play2714@sina.cn",
      long_description=readme_file(),
      license="MIT",
      url="https://www.juyerhy.com/PythonCode")














