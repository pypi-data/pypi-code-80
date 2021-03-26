from distutils.core import setup

setup(
    name='tgam-com',
    packages=['aws'],
    version='0.1',
    description='The Globe and Mail',
    author='Aras Azimipanah',
    author_email='aazimipanah@globeandmail.com',
    url='https://github.com/globeandmail/tgam-com',
    download_url='https://github.com/joelbarmettlerUZH/Scrapeasy/archive/pypi-0_1_3.tar.gz',
    keywords=['aws', 's3'],
    install_requires=[
        'boto3',
    ],
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        # 'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.4',
        # 'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.7',
    ],
)
