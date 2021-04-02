# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logmail']

package_data = \
{'': ['*']}

install_requires = \
['emails>=0.6,<0.7', 'loguru>=0.5.3,<0.6.0']

setup_kwargs = {
    'name': 'logmail',
    'version': '0.1.0',
    'description': 'Simple send mails as logging in Loguru',
    'long_description': 'logmail\n========\n\nA simple package for sending emails (as simple, as writing logs with [loguru](https://github.com/Delgan/loguru))\n\nInstall\n-------\n```\npip install logmail\n```\n\nor with [poetry](https://python-poetry.org/):\n```\npoetry add logmail\n```\n\nUsage\n-----\nSetting global config:\n\n```\nfrom logmail import mailer\n\nmailer.set_mail_config(\n    smtp_host="mail.example.com",\n    smtp_port=25,\n    smtp_timeout=2,\n    service_name="AWESOME SERVICE",\n    recipient_list=["foo@example.com", "bar@example.com"],\n    mail_from="Cool Mailer <noreply-some-service@example.com>",\n)\n```\n\nFrom any *.py file in your awesome project:\n```\nfrom logmail import mailer\n\nmailer.debug("This is debug message!")\nmailer.info("This is info message!")\nmailer.success("This is success message!")\nmailer.warning("This is warning message!")\nmailer.error("This is error message!")\nmailer.critial("This is critial message!")\n```\n\nIf you need to send email with custom params:\n```\nfrom logmail import mailer\n...\nmailer.send_mail(\n    subject="Some subject", \n    message="Some message",  # may be html string\n    mail_from="Mr Foo <foo@example.com>",\n    recipient_list=["fizzbuzz@example.com"]\n)\n```\n\n\n\nAdvanced usage\n--------------\n\nYou may see debugging info while sending emails by:\n```\nfrom logmail import mailer\n\n...\n\nwith mailer.debugging():\n    mailer.info("Mail sent with debugging this process")\n\n```\n\nYou may easily set production and testing config by:\n```\nfrom logmail import mailer\n\nmailer.set_mail_config(\n    smtp_host="mail.example.com",\n    smtp_port=25,\n    smtp_timeout=2,\n    service_name="AWESOME SERVICE",\n    recipient_list=["foo@example.com", "bar@example.com"],\n    mail_from="Cool Mailer <noreply-some-service@example.com>",\n    testing=True,\n    test_service_name="SOME TEST SERVICE",\n    test_recipient_list=["testfoo@example.com", "testbar@example.com"],\n    test_mail_from="Testing Cool Mailer <test-noreply-some-service@example.com>",\n)\n```\n\nSetting global debugging while sending mails:\n```\nfrom logmail import mailer\n\n# in initialization time\nmailer.set_mail_config(\n    ...\n    debug=True\n)\n\n# in other place\nmailer.set_debug(debug=True)\n```\n\n\nYou may also set limit of exceptions in traceback (if it was raised):\n```\nfrom logmail import mailer\n\n# in initialization time\nmailer.set_mail_config(\n    ...\n    trackeback_limit=666\n)\n\n# in other place\nmailer.set_trackeback_limit(666)\n```\n\nIf you need to convert subject and message to html by default, try this:\n```\nfrom logmail import mailer\n\n# in initialization time\nmailer.set_mail_config(\n    ...\n    convert_all_data_to_html=True\n)\n\n# in other place\nmailer.set_convert_all_data_to_html(True)\n```\n*Note: logmail will apply **convert_str_to_html** method to subject and message with its default params every time when logmail sends not custom message*',
    'author': 'DanilaCharushin',
    'author_email': 'charushin2000@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DanilaCharushin/logmail',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
