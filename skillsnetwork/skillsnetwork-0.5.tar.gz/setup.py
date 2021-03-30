from setuptools import setup

setup(
    name='skillsnetwork',
    version='0.5',
    license='BSD',
    author='Bradley Steinfeld',
    author_email='bs@ibm.com',
    url='http://vision.skills.network',
    long_description="README.md",
    packages=['skillsnetwork'],
    scripts=['bin/cvstudio_report','bin/cvstudio_ping'],
    install_requires=['requests','ibm-cos-sdk==2.0.1','tqdm','pandas','torch','Pillow'],
    description="Skills Network",
)
