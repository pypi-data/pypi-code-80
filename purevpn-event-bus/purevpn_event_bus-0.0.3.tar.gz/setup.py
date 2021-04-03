from distutils.core import setup
import setuptools


setup(
    name='purevpn_event_bus',
    packages=['purevpn_event_bus'],
    version='0.0.3',
    license='MIT',
    description='',
    author='Syed Hammad Ahmed',
    author_email='syed.ahmed@purevpn.com',
    url='https://github.com/sha-gaditek/purevpn_event_bus',
    download_url='https://github.com/sha-gaditek/purevpn_event_bus/archive/refs/tags/0.0.3.tar.gz',
    keywords=[
        'DDD',
        'Event Bus'
    ],
    install_requires=[
        'shortuuid'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8'
    ]
)
