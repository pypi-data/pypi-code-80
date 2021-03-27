from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

REQUIRES = [
  "urllib3 >= 1.25.3",
  "python-dateutil",
]

setup(
    name='SWX-API-Python-SDK',
    version='0.16',
    description='Smartworks API SDK for Python',
    author='Smartworks SDK TF',
    author_email='',
    url='',
    python_requires='>=3.6',
    install_requires=REQUIRES,
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]
)
