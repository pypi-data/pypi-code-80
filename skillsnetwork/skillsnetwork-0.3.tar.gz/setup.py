from setuptools import setup

setup(
    name='skillsnetwork',
    version='0.3',
    license='BSD',
    author='Bradley Steinfeld',
    author_email='bs@ibm.com',
    url='http://vision.skills.network',
    long_description="README.txt",
    packages=['skillsnetwork'],
    scripts=['bin/cvstudio_report'],
    install_requires=['requests'],
    description="Skills Network",
)