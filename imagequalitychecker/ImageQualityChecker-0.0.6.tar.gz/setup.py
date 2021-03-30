from setuptools import setup, find_packages

VERSION = '0.0.6'
DESCRIPTION = 'VinAI image quality checker'
LONG_DESCRIPTION = 'Classify normal, soil, defocusing images'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="ImageQualityChecker",
    version=VERSION,
    author="Hieu Tr Luu",
    author_email="<hieu.luu2411@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    package_data={'checker': ['*.onnx']},
    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    install_requires=[
        'numpy>=1.18.5',
        'albumentations>=0.5.2',
        'opencv-python>=4.5.1',
        'onnxruntime>=1.3.0'
    ]
)