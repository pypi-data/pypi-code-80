from setuptools import setup, find_packages
import sys
import subprocess
import setuptools

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


CUSTOM_COMMANDS = [['echo', 'Custom command worked!']]


class CustomCommands(setuptools.Command):
    """A setuptools Command class able to run arbitrary commands."""
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def RunCustomCommand(self, command_list):
        print('Running command: %s' % command_list)
        p = subprocess.Popen(
            command_list,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        # Can use communicate(input='y\n'.encode()) if the command run requires
        # some confirmation.
        stdout_data, _ = p.communicate()
        print('Command output: %s' % stdout_data)
        if p.returncode != 0:
            raise RuntimeError('Command %s failed: exit code: %s' % (command_list, p.returncode))

    def run(self):
        for command in CUSTOM_COMMANDS:
            self.RunCustomCommand(command)


setup(
    name='harp-agent',
    python_requires='>3.7.0',
    version='1.0.4',
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
    cmdclass={
        # Command class instantiated and run during pip install scenarios.
        'CustomCommands': CustomCommands,
    },
    data_files=[
        ('/etc/init.d', [
            'data/init-script/harp-agent'
        ])
    ]
)
