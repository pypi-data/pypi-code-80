from setuptools import setup, find_packages

setup(
    name='PNGtoGIF',
    version='1.0.3',
    description='Test package for distribution',
    author='Eunki7',
    author_email='outsider7224@gmail.com',
    url='',
    download_url='',
    install_requires=['pillow'],
    include_package_data=True,
    packages=find_packages(),
    keywords=['PNGtoGIF', 'pngtogif'],
    python_requires='>=3',
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
