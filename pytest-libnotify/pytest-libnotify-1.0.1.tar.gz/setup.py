import setuptools

setuptools.setup(
    name="pytest-libnotify",
    version="1.0.1",
    url="https://github.com/moser/pytest-libnotify",

    author="Martin Vielsmaier",
    author_email="moser@moserei.de",

    description="Pytest plugin that shows notifications about the test run",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords=[],
    packages=setuptools.find_packages(),
    install_requires=['pytest'],
    setup_requires=['pytest-runner'],
    tests_require=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    entry_points={
        'pytest11': ['notifier = pytest_libnotify'],
    },
)
