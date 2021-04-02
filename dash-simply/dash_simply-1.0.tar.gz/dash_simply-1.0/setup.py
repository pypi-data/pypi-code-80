import setuptools

setuptools.setup(
    name = 'dash_simply',
    packages = ['/Users/cinema/Desktop/Projects/dash_simply'],
    version = '1.0',  # Ideally should be same as your GitHub release tag varsion
    description = 'Create dash view objects easily with reusable methods.',
    author = 'Enun Bassey Enun',
    author_email = 'enunenun21@gmail.com',
    url = 'https://github.com/EJ-enun/dash_simply/',
    download_url = 'https://github.com/EJ-enun/dash_simply/archive/refs/tags/1.0.0.tar.gz',
    keywords = ['Dash', 'Python'],
    project_urls={
        "Bug Tracker": "https://github.com/EJ-enun/dash_simply/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    #package_dir={"/Users/cinema/Desktop/Projects/dash_simply": "src"},
    #packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6"
)
