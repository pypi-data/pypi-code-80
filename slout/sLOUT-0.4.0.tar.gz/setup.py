# sLOUT by Sidpatchy
# A small helper library used in several of my projects
# If you experience any issues, please open an issue on the GitHub: https://github.com/Sidpatchy/sLOUT

from setuptools import setup, find_packages

setup(
    name='sLOUT',
    version='0.4.0',
    description='A small helper library used in several of my projects',
    url='https://github.com/Sidpatchy/sLOUT',
    author='Sidpatchy',
    license='MIT License',
    packages=['sLOUT'],
    install_requires=['pyyaml'],
#    python_requires=">=3.4",

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
)