from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='ednevnik',
    version='0.0.1',
    description='A very basic E-Dnevnik API.',
    long_description=open('README.md').read(),
    long_description_content_type = 'text/markdown',
    author='Parzival',
    license='MIT',
    classifiers=classifiers,
    keywords='ednevnik',
    packages=find_packages(),
    install_requires=['selenium']
)