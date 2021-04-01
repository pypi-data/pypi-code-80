from setuptools import setup

setup(
    name='intentBox',
    version='0.2a1',
    packages=['intentBox'],
    url='https://github.com/HelloChatterbox/intentBox',
    license='',
    author='jarbasai',
    install_requires=["adapt-parser>=0.3.3",
                      "padatious>=0.4.6",
                      "fann2>=1.0.7",
                      "padaos>=0.1.9",
                      "requests"],
    author_email='jarbasai@mailfence.com',
    description='chatterbox intent parser, extract multiple intents from a single utterance '
)
