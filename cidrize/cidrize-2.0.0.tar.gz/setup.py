# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['cidrize']
install_requires = \
['netaddr>=0.8.0,<0.9.0']

entry_points = \
{'console_scripts': ['cidr = cidrize:main']}

setup_kwargs = {
    'name': 'cidrize',
    'version': '2.0.0',
    'description': 'Cidrize parses IPv4/IPv6 addresses, CIDRs, ranges, and wildcard matches & attempts to return a valid list of IP addresses',
    'long_description': '=======\nCidrize\n=======\n\nIP address parsing for humans.\n\nCidrize takes IP address inputs that people tend to use in practice, validates\nthem, and converts them to objects.\n\nIntelligently parses IPv4/IPv6 addresses, CIDRs, ranges, and wildcard matches to\nattempt return a valid list of IP addresses.\n\nThe ``cidrize()`` function does all the work trying to parse IP addresses correctly.\n\n============\nInstallation\n============\n\nYou can install ``cidrize`` via Pip::\n\n    pip install cidrize\n\n============\nDependencies\n============\n\nCidrize is basically a thin veneer around `netaddr <http://pypi.python.org/pypi/netaddr/>`_ to provide a human layer for parsing IP addresses.\n\n=====\nUsage \n=====\n\nSupported input formats\n-----------------------\n\nInput is very flexible and can be of any of the following formats::\n\n    192.0.2.18  \n    192.0.20.64/26\n    192.0.2.80-192.0.2.85\n    192.0.2.170-175\n    192.0.2.8[0-5]\n    192.0.2.[5678]\n\nHyphenated ranges do not need to form a CIDR block but the starting number must\nbe of lower value than the end. The ``netaddr`` module does most of the heavy\nlifting for us here.\n\nUnsupported formats\n-------------------\n\nNetwork mask (e.g. 192.0.2.0 255.255.255.0) and host mask (aka reverse mask,\n192.0.2.0 0.0.0.255) notation are not accepted at this time.\n\nThe cidrize function returns a list of consolidated ``netaddr.IPNetwork``\nobjects. By default parsing exceptions will raise a ``CidrizeError`` (with\ndefault argument of ``raise_errors=True``). You may pass ``raise_errors=False`` to cause\nexceptions to be stripped and the error text will be returned as a list. This\nis intended for use with scripts or APIs where receiving exceptions would not\nbe preferred.\n\nThe module may also be run as a script for debugging purposes.\n\nThe cidrize function\n--------------------\n\nFire up your trusty old Python interpreter and follow along!\n\n::\n\n    >>> from cidrize import cidrize\n\nOld-fashioned CIDR\n------------------\n\n::\n\n    >>> cidrize("1.2.3.4")\n    [IPNetwork(\'1.2.3.4/32\')]\n\nHyphenated range (default, strict=False)\n----------------------------------------\n\n::\n\n    >>> cidrize("2.4.6.8-2.4.6.80")\n    [IPNetwork(\'2.4.6.0/25\')]\n\nHyphenated range strict (strict=True)\n----------------------------------------\n\n::\n\n    >>> cidrize("2.4.6.8-2.4.6.80", strict=True)\n    [IPNetwork(\'2.4.6.8/29\'), IPNetwork(\'2.4.6.16/28\'), \n    IPNetwork(\'2.4.6.32/27\'), IPNetwork(\'2.4.6.64/28\'), \n    IPNetwork(\'2.4.6.80/32\')]\n\nWildcard\n--------\n\nYou may provide wildcards using asterisks. This is limited to the 4th and final octet only::\n\n    >>> cidrize("15.63.148.*")\n    [IPNetwork(\'15.63.148.0/24\')]\n\nBracketed range\n---------------\n\n::\n\n    >>> cidrize("21.43.180.1[40-99]")\n    [IPNetwork(\'21.43.180.140/30\'), IPNetwork(\'21.43.180.144/28\'), \n    IPNetwork(\'21.43.180.160/27\'), IPNetwork(\'21.43.180.192/29\')]\n\nBad!\n----\n\nBad CIDR prefixes are rejected outright::\n\n    >>> cidrize("1.2.3.38/40")\n    Traceback (most recent call last):\n    File "<stdin>", line 1, in <module>\n    File "cidrize.py", line 145, in cidrize\n        raise CidrizeError(err)\n    cidrize.CidrizeError: CIDR prefix /40 out of range for IPv4!\n\nWack range?!\n------------\n\nRanges must always start from lower to upper bound, or this happens::\n\n    >>> cidrize("1.2.3.4-0")\n    Traceback (most recent call last):\n      File "<stdin>", line 1, in <module>\n      File "cidrize.py", line 145, in cidrize\n        raise CidrizeError(err)\n    cidrize.CidrizeError: lower bound IP greater than upper bound!\n\n=========\nCidr Tool\n=========\n\nThe cidrize package also comes with the ``cidr`` command, which has two basic operations. \n\nSimple output::\n\n    % cidr 1.2.3.4/30\n    1.2.3.4/30\n\nVerbose output::\n\n    % cidr -v 1.2.3.4/30\n    Spanning CIDR:          1.2.3.4/30\n    Block Start/Network:    1.2.3.4\n    1st host:               1.2.3.5\n    Gateway:                1.2.3.6\n    Block End/Broadcast:    1.2.3.7\n    DQ Mask:                255.255.255.252\n    Cisco ACL Mask:         0.0.0.3\n    # of hosts:             2\n    Explicit CIDR blocks:   1.2.3.4/30\n\nAnd that\'s that!\n\n=======\nLicense\n=======\n\nCidrize is licensed under the `BSD 3-Clause License <http://www.opensource.org/licenses/BSD-3-Clause>`_. Please see ``LICENSE.rst``\nfor the details.\n',
    'author': 'Jathan McCollum',
    'author_email': 'jathan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jathanism/cidrize/',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
