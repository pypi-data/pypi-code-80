from setuptools import setup, find_packages

setup(
    name="smay_ros",
    version="0.0.1",
    keywords=("pip", "smay", "ros", "smay_ros"),
    description="A ROS manager based on smay",
    long_description="A ROS manager based on smay",
    license="MIT Licence",

    url="https://github.com/xkgeng/smay_ros",
    author="Geng Xinkuang",
    author_email="",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["smay", "rospy"]
)
