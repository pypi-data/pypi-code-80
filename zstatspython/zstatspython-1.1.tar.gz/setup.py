import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zstatspython",
    version="1.1",
    author="Astrogamer54",
    author_email="mail@astrogamer54.com",
    description="Get Player Data From zstats plugin. Not An Official Plugin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Astrogamer54/zstatspython",
    packages=setuptools.find_packages(),
    install_requires=[
    	'mysql-connector-python',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
