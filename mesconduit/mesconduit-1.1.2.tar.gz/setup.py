
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mesconduit",                     # This is the name of the package
    version="1.1.2",                        # The initial release version
    author="Melvin Paul Miki",                     # Full name of the author
    description="Python & Conduit Integration Library",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=[''],    # List of all python modules to be installed
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["mesconduit"],             # Name of the python package
    package_dir={'':'conduit'},     # Directory of the source code of the package
    install_requires=["requests","logging","json","os"]                 # Install other dependencies if any
)


