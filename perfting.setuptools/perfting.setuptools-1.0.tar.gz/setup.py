from perfting.setuptools import Package

Package(
    name = "perfting.setuptools",
    version = "1.0",
    description = Package.Description(
        "better setuptools with type hinting support"
    ),
    license = "MIT",
    url = Package.URL(
        home = "https://github.com/perfting/setuptools"
    ),
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Build Tools",
        "Framework :: Setuptools Plugin",
    ],
    packages = Package.Packages(
        "perfting.setuptools",
        data = {
            "perfting.setuptools": [
                "py.typed"
            ]
        },
        namespaces = [
            "perfting"
        ]
    )
).setup()