import setuptools

setuptools.setup(
    name="PIPWeb",
    version="2021.3.3",
    maintainer="Rajdeep Malakar",
    maintainer_email="Rajdeep@tgeeks.cf",
    author="TechGeeks",
    author_email="TechGeeks@tgeeks.cf",
    description="A Open-Source & Free Python PIP GUI (Web) Installer",
    url="https://github.com/TechGeeks-Dev/PIPWeb",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires = [
        'Flask'
    ],
    entry_points=dict(
        console_scripts=['pipweb=PIPWeb.app:main']
    )
)
