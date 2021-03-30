# python3 setup.py sdist upload -r testpypi
# pip install -i https://test.pypi.org/simple/ lins_pix==0.0.14

from distutils.core import setup
from setuptools import find_packages


def get_version():
    return open('version.txt', 'r').read().strip()


# def get_requirements():
#     return [i.strip() for i in open('requirements-pix.txt').readlines()]


setup(
    name='lins_pix',
    description='Pacote para gerenciar transacoes PIX',
    version= get_version(),
    packages=find_packages(),
    install_requires=[
        'qrcode==6.1',
        'Pillow==8.0.1',
        'requests==2.25.1',
        'PyJWT==1.7.1',



    ],  # get_requirements(),
    url='https://bitbucket.org/grupolinsferrao/pypck-pix/',
    author='Gustavo Schaedler',
    author_email='gustavopoa@gmail.com',
    license='MIT',
)
