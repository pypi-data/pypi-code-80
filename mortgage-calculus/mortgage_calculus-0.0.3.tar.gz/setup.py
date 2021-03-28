from setuptools import setup, find_packages

def readme():
      with open("README.rst") as f:
            return f.read()

setup(name="mortgage_calculus",
      version="0.0.3",
      description="Tools for the analysis of mortgages",
      long_description=readme(),
      long_description_content_type="text/markdown",
      classifiers=[
        "License :: OSI Approved :: MIT License"
      ],
      keywords="mortgage cashflows annuity interest",
      url="http://github.com/ramonVDAKKER/mortgage_calculus",
      author="Ramon van den Akker",
      author_email="ramon@vandenakker.tech",
      license="MIT",
      packages=find_packages(include=["mortgage_calculus"]),
      install_requires=["numpy", "pandas", "typing"],
      python_requires= ">=3.7",
      setup_requires=["pytest-runner", "flake8"],
      tests_require=["pytest"],
     # extras_require={"dev": ["pywin32 >=1.0", "ipykernel", "notebook", "jupyterlab"]}
      )
