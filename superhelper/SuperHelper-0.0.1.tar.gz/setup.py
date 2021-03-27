from setuptools import setup, find_packages

with open("README.md") as fp:
    long_desc = fp.read()

setup(
    name="SuperHelper",
    version="0.0.1",
    author="Nguyen Thai Binh",
    author_email="binhnt.mdev@gmail.com",
    description="A collection of Python CLI to make life easier for terminal geeks!",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/GreaterGoodCorp/FocusEnabler",
    project_urls={
        "Bug Tracker": "https://github.com/GreaterGoodCorp/FocusEnabler/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Home Automation",
        "Topic :: Office/Business",
        "Topic :: Utilities",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    entry_points={
        "console_scripts": ["helper = SuperHelper.Core:main_entry"],
    },
    install_requires=[
        "click",
        "colorama",
    ],
    python_requires=">=3.6",
)
