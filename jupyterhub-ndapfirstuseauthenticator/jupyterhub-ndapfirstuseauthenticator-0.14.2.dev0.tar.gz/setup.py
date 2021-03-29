import os

from setuptools import setup, find_packages

# Get the current package version.
here = os.path.abspath(os.path.dirname(__file__))
version_ns = {}
with open(os.path.join(here, 'ndapfirstuseauthenticator', '_version.py')) as f:
    exec(f.read(), {}, version_ns)

setup(
    name='jupyterhub-ndapfirstuseauthenticator',
    version=version_ns['__version__'],
    description='NDAP Token Authenticator and JupyterHub Authenticator that lets users set passwords on first use',
    long_description=open("README.md").read(),
    url='https://github.com/manu625/jupyterhub-ndapauthenticator',
    author='manu625',
    author_email='im.manu625@gmail.com',
    license='3 Clause BSD',
    packages=find_packages(),
    install_requires=['bcrypt', 'jupyterhub>=0.8', 'requests'],
    package_data={
        '': ['*.html'],
    },
)
