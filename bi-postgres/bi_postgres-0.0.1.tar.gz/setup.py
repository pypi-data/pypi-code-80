from distutils.core import setup


setup(
    name='bi_postgres',
    packages=['bi_postgres'],
    version='0.0.1',
    license='MIT',
    description='TYPE YOUR DESCRIPTION HERE',
    author='Syed Hammad Ahmed',
    author_email='syed.ahmed@purevpn.com',
    url='https://bitbucket.org/sha31/bi_postgres',
    download_url='https://github.com/sha-gaditek/bi_postgres/archive/refs/tags/0.0.2.tar.gz',
    keywords=[
        'Postgres',
        'SqlAlchemy'
    ],
    install_requires=[
        'sqlalchemy'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8'
    ]
)
