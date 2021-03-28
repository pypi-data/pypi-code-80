from setuptools import setup, find_packages
setup(
    name = 'file-zilla',
    version = '1.0',
    scripts = ['./script/fm'],
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