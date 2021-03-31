from setuptools import setup, find_packages
import sys

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 7)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================
This version of Harp Agent requires Python {}.{}, but you're trying to
install it on Python {}.{}.
Please install Python version >=3.7
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)


with open('requirements.txt') as f:
    requirements = f.read().splitlines()


tests_require = ['test'],


setup(
    name='harp-agent',
    python_requires='>3.7.0',
    version='1.0.1',
    description="Harp Agent",
    url='',
    include_package_data=True,
    author='',
    author_email='',
    classifiers=[
    ],
    keywords=[],
    packages=find_packages(),
    install_requires=requirements,
    tests_require=tests_require,
    entry_points={
        'console_scripts': [
            'harp-agent = harp_agent.app:main',
            'harp-agent-add = cmd_command.agent_configuration:agent_add',
            'harp-agent-update = cmd_command.agent_configuration:agent_update',
            'harp-agent-delete = cmd_command.agent_configuration:agent_delete',
        ]
    },
    zip_safe=False,
    cmdclass={},
    data_files=[
        ('/etc/init.d', [
            'data/init-script/harp-agent'
        ])
    ]
)
