# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arrakisapi',
 'arrakisapi.api',
 'arrakisapi.healthcheck',
 'arrakisapi.internal',
 'arrakisapi.tests',
 'arrakisclient',
 'arrakisclient.dsl',
 'arrakisclient.tests',
 'arrakisclient.types',
 'arrakisclient.types.tests']

package_data = \
{'': ['*']}

install_requires = \
['async_generator>=1.10,<2.0',
 'grpcio==1.34.0',
 'mock>=4.0.3,<5.0.0',
 'protobuf>=3.14.0,<4.0.0',
 'typing-extensions>=3.7.4,<4.0.0']

extras_require = \
{':python_version < "3.7"': ['dataclasses>=0.6']}

setup_kwargs = {
    'name': 'authzed',
    'version': '0.2.0',
    'description': 'Client library for the Authzed service.',
    'long_description': '# Authzed-py\n\nThe Python client library for Authzed.\n\n## Example Usage\n\n### QuickStart\n\nA complete version of this example can be found in this repository at [`examples/basic.py`](examples/basic.py)\n\nIn Python, we have support for declaring ORM-like models which allow you to easily interact with\nthe data in your tenant. Here we define some models for `User` and `Document` which match the\ntenant namespace configuration.\n\n```py\nfrom arrakisclient.types.namespace import ArrakisNamespace, Relation\n\n\n# Define some ORM-like models, must match the namespaces configured in the tenant\nclass ReferenceableNamespace(ArrakisNamespace):\n    """Base model that will define the "ellipsis" relation, which can be used to reference items\n    in the namespace as a unit, without implying any further relationships."""\n\n    ellipsis = Relation(relation_name="...")\n\n\nclass User(ReferenceableNamespace):\n    """ A model to represent users in your domain. """\n\n    __namespace__ = "yourtenant/user"\n\n\nclass Document(ArrakisNamespace):\n    """ A model to represent documents in your business domain (if you have such a thing). """\n\n    __namespace__ = "yourtenant/document"\n\n    # These relations define the permissions your code will ask about\n    read = Relation(User)\n    write = Relation(User)\n    delete = Relation(User)\n\n    # These relations define the relationship (role) a user can be directly granted\n    viewer = Relation(User)\n    contributor = Relation(User)\n    owner = Relation(User)\n```\n\nNow that we have our models, let\'s instantiate a client that will use them:\n\n```py\nfrom arrakisclient.client import ArrakisClient\n\ntoken = "t_your_token_here_1234567deadbeef"\nclient = ArrakisClient(User, Document, access_token=token)\n```\n\nAnd now we can use our ORM-like models to mutate the data in the tenant:\n\n```py\n# Create some object references\na_doc = Document("doc1")\nan_owner = User("theowner")\nan_editor = User("userwhocanedit")\na_viewer = User("viewonlyuser")\n\n# Insert some tuples granting roles to users\nwith client.batch_write() as w:\n    w.create(a_doc.owner(an_owner.ellipsis))\n    w.create(a_doc.contributor(an_editor.ellipsis))\n    w.create(a_doc.viewer(a_viewer.ellipsis))\n\n# Save the zookie that the call above generated to prevent new enemies\n# We recommend saving this from any call to batch_write or content_change_check,\n# and storing it alongside the object referenced in the write or check (in this case a_doc)"\nwhen_perms_changed = w.revision\n```\n\nNow we can run some permissions checks on the date in the model to verify that it matches our expectations:\n\n```py\nfrom arrakisclient.types.tuple import ArrakisUserset\n\n# Run some checks\nassert client.check(a_doc.read, ArrakisUserset.from_onr(a_viewer.ellipsis), when_perms_changed)\nassert client.check(a_doc.read, ArrakisUserset.from_onr(an_editor.ellipsis), when_perms_changed)\nassert client.check(a_doc.read, ArrakisUserset.from_onr(an_owner.ellipsis), when_perms_changed)\nassert not client.check(a_doc.write, ArrakisUserset.from_onr(a_viewer.ellipsis), when_perms_changed)\nassert client.check(a_doc.write, ArrakisUserset.from_onr(an_editor.ellipsis), when_perms_changed)\nassert client.check(a_doc.write, ArrakisUserset.from_onr(an_owner.ellipsis), when_perms_changed)\nassert not client.check(\n    a_doc.delete, ArrakisUserset.from_onr(a_viewer.ellipsis), when_perms_changed\n)\nassert not client.check(\n    a_doc.delete, ArrakisUserset.from_onr(an_editor.ellipsis), when_perms_changed\n)\nassert client.check(a_doc.delete, ArrakisUserset.from_onr(an_owner.ellipsis), when_perms_changed)\n```\n',
    'author': 'Petricorp',
    'author_email': 'support@petricorp.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
