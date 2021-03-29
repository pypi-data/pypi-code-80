import setuptools

prj = 'snifa'

import os, sys
environment_variable_name = 'VERSION'
environment_variable_value = os.environ.get( environment_variable_name, None )

if environment_variable_value is not None:
    sys.stdout.write( "Using '%s=%s' environment variable!\n" % (
            environment_variable_name, environment_variable_value ) )
else:
    environment_variable_value = '0.0.1'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name=prj,
    version="%s" % (environment_variable_value),
    author="Flavio Abreu Araujo",
    author_email="flavio.abreuaraujo@uclouvain.be",
    url="https://gitlab.flavio.be/flavio/" + prj,
    description="Simple Numerical Instantaneous Frequency Approximation (SNIFA)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=[prj],
    classifiers=[
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development",
        "Topic :: Scientific/Engineering",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'scipy',
    ],
)
