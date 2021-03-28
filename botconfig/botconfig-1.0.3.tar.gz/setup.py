from setuptools import setup, find_packages

setup(
    name="botconfig",
    version="1.0.3",
    description="A simple discord bot configuration utility",
    long_description=open("README.md").read(),
    author="tag-epic",
    author_email="tagepicuwu@gmail.com",

    project_urls={
        "GitHub": "https://github.com/discollaboration/BotConfigLib",
        "Website": "https://config.farfrom.world"
    },

    packages=find_packages(),
    install_requires=["speedcord"]
)
