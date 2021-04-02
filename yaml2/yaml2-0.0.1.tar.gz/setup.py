import setuptools
    
setuptools.setup(
    name="yaml2",
    version="0.0.1",
    author="TCYT",
    description="Lobby bot.",
    url="https://www.youtube.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'crayons',
        'fortnitepy',
        'BenBotAsync',
        'FortniteAPIAsync',
        'uvloop==0.15.2',
        'sanic',
        'colorama',
        'aiohttp',
        'requests'
    ],
)
