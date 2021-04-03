import setuptools


setuptools.setup(
    name="ofpubsub",
    version="0.3",
    author="Adi Aswara",
    author_email="a.aswara@gmail.com",
    description="OnlyFunction PubSub",
    long_description="OnlyFunction PubSub",
    long_description_content_type="text/markdown",
    url="https://github.com/aswara/of-pubsub",
    install_requires=['requests'],
    packages=['ofpubsub'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
     python_requires='>=3.5',
)