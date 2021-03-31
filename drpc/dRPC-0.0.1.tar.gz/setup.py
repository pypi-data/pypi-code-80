from setuptools import setup, find_packages

setup(
    name="dRPC",
    version='0.0.1',
    author="WEN",
    description="",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/GoodManWEN/dRPC",
    packages = find_packages(),
    install_requires = [],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Framework :: AsyncIO',
    ],
    python_requires='>=3.4',
    keywords=["dRPC",]
)