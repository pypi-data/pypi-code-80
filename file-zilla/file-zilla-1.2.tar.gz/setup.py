from setuptools import setup, find_packages
setup(
    name = 'file-zilla',
    version = '1.2',
    scripts = ['./script/file-zilla'],
    author = 'Gaurav Arora',
    description = ('File manager'),
    packages = ['file-zilla'],
    install_requires=[
        'setuptools',
        'PyPDF2 >= 1.26.0',
        'Pillow >= 7.0.0'
    ],
    python_requires='>=3.7'
)