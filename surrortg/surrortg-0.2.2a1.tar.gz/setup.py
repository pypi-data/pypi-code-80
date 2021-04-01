import setuptools
__version__ = "0.2.2a1"


def get_requirements(name):
    with open(name) as f:
        lines = f.read().splitlines()
    return [line for line in lines if not line.lstrip().startswith("#")]


setuptools.setup(
    name="surrortg",
    version=__version__,
    install_requires=get_requirements("requirements.txt"),
    extras_require={
        "dev": get_requirements("requirements-dev.txt"),
    },
    author="SurrogateInc",
    description="SurroRTG SDK",
    url="https://github.com/SurrogateInc/surrortg-sdk",
    packages=setuptools.find_packages(include="surrortg"),
    python_requires=">=3.7",
)
