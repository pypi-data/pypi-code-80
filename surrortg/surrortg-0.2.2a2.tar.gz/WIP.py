# cat requirements.txt | grep -v '^[# \n]'
reqular = """
aiohttp==3.7.4
async-timeout==3.0.1
attrs==20.3.0
chardet==3.0.4
idna==2.10
multidict==5.1.0
pigpio==1.78
python-engineio==3.14.2
python-socketio==4.6.1
pyyaml==5.4.1
six==1.15.0
toml==0.10.2
typing-extensions==3.7.4.3
yarl==1.6.3
"""


# cat requirements-dev.txt | grep -v '^[# \n]'
dev = """
alabaster==0.7.12
appdirs==1.4.4
attrs==20.3.0
babel==2.9.0
black==20.8b1
certifi==2020.12.5
cfgv==3.2.0
chardet==3.0.4
click==7.1.2
codespell==v2.0.0
commonmark==0.9.1
distlib==0.3.1
docutils==0.16
filelock==3.0.12
flake8-polyfill==1.0.2
flake8==3.9.0
identify==2.2.2
idna==2.10
imagesize==1.2.0
importlib-metadata==3.10.0
isort==5.7.0
jinja2==2.11.3
markdown-it-py==0.6.2
markupsafe==1.1.1
mccabe==0.6.1
mdit-py-plugins==0.2.6
mypy-extensions==0.4.3
myst-parser==0.13.5
packaging==20.9
pathspec==0.8.1
pep517==0.10.0
pep8-naming==0.11.1
pip-tools==6.0.1
pre-commit==2.11.1
pycodestyle==2.7.0
pyflakes==2.3.1
pygments==2.8.1
pyparsing==2.4.7
pytz==2021.1
pyyaml==5.4.1
recommonmark==0.6.0
regex==2021.3.17
requests==2.25.1
six==1.15.0
snowballstemmer==2.1.0
sphinx-rtd-theme==0.4.3
sphinx==3.1.1
sphinxcontrib-applehelp==1.0.2
sphinxcontrib-devhelp==1.0.2
sphinxcontrib-htmlhelp==1.0.3
sphinxcontrib-jsmath==1.0.1
sphinxcontrib-qthelp==1.0.3
sphinxcontrib-serializinghtml==1.1.4
toml==0.10.2
typed-ast==1.4.2
typing-extensions==3.7.4.3
urllib3==1.26.4
virtualenv==20.4.3
zipp==3.4.1
"""
print(
    """
[build-system]
requires = ["flit_core >=2,<4"]
build-backend = "flit_core.buildapi"

[tool.flit.metadata]
module = "surrortg"
author = "Surrogate Inc"
home-page = "https://github.com/SurrogateInc/surrortgsdk-sdk"
classifiers = ["License :: OSI Approved :: MIT License"]
requires = ["""
)

for line in reqular.split("\n"):
    if line != "":
        print(f'    "{line}",')

print(
    """
]

[tool.flit.metadata.requires-extra]
dev = ["""
)

for line in dev.split("\n"):
    if line != "":
        print(f'    "{line}",')

print("]")
