from setuptools import setup, find_packages

setup(
    name="foundry_ml_cli",
    version="0.0.1",
    packages=find_packages(),
    install_requires=["click", "joblib", "dlhub_sdk", "foundry_ml"],
    entry_points={"console_scripts": ["foundry = foundry_cli:install"]},
    # descriptive info, non-critical
    description="Foundry CLI",
    long_description=open("README.md").read(),
    author="Ben Blaiszik",
    author_email="blaiszik@uchicago.edu",
    url="https://github.com/MLMI2-CSSI/foundry-cli",
    python_requires=">=3.5",
)
