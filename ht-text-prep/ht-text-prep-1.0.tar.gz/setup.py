import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='ht-text-prep',  
    version='1.0',
    #scripts=['htrc-text-processing'] ,
    author="Ashan Liyanage, Ryan Dubnicek, HathiTrust Research Center",
    author_email="ashan8k@gmail.com, rdubnic2@illinois.edu, htrc-help@hathitrust.org",
    description="Tools for management and processing of HathiTrust text data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/htrc/ht-text-prep",
    packages=setuptools.find_packages(),
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: University of Illinois/NCSA Open Source License",
         "Operating System :: OS Independent",
         ],
    python_requires='>=3.6',
 )
