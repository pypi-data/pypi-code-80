import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="liftpose",
    version="0.2",
    author="Adam Gosztolai & Semih Gunel",
    packages=["liftpose", "liftpose.lifter"],
    description="Monocular 3D pose Estimation on Labatoary Animals",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NeLy-EPFL/LiftPose3D"
)
