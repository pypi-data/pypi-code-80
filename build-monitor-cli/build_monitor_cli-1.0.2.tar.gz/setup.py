from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name = "build_monitor_cli",
    version = "1.0.2",
    author = "Zhen Tian",
    author_email = "zhen.tian@thoughtworks.com",
    description = 'Azure devops builds commandline monitor',
    license = "BSD",
    keywords = "azure devops",
    url = 'https://github.com/dawncold/build_monitor_cli',
    packages=['build_monitor_cli'],
    long_description = 'Azure devops builds commandline monitor',
    entry_points = {
        'console_scripts': [
            'bmonitor = build_monitor_cli:entry'
        ]
    },
    install_requires=requirements,
    python_requires='>=3.5',
    classifiers=[
        "Development Status :: 4 - Beta",
        'Environment :: Console',
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
