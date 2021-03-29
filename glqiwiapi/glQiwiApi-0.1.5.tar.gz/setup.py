import setuptools

import glQiwiApi

setuptools.setup(
    name="glQiwiApi",  # Replace with your own username
    version=glQiwiApi.__version__,
    author="GLEF1X",
    author_email="glebgar567@gmail.com",
    description="Parser for post and get requests",
    long_description='Light and fast wrapper for qiwi bills',
    long_description_content_type="text/x-rst",
    url="https://github.com/GLEF1X/parser",
    packages=['glQiwiApi'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "aiohttp==3.7.3",
        "aiosocksy==0.1.2",
        'aiofiles==0.6.0',
        "wheel",
        "pytz"
    ],
    python_requires=">=3.6",
)
