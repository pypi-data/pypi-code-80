from setuptools import setup, find_packages
setup(
    name = 'filezilla',
    version = '1.0',
    scripts = ['./script/filezilla'],
    author = 'Gaurav Arora',
    description = ('File manager'),
    packages = ['filezilla'],
    install_requires=[
        'setuptools',
        'PyPDF2 >= 1.26.0',
        'Pillow >= 7.0.0'
    ],
    python_requires='>=3.7'
)