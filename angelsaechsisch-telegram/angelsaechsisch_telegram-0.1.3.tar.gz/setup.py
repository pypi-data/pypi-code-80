# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['angelsaechsisch_telegram']

package_data = \
{'': ['*'],
 'angelsaechsisch_telegram': ['data/antworten.txt',
                              'data/antworten.txt',
                              'data/antworten.txt',
                              'data/antworten.txt',
                              'data/ausnahmen.txt',
                              'data/ausnahmen.txt',
                              'data/ausnahmen.txt',
                              'data/ausnahmen.txt',
                              'data/de.txt',
                              'data/de.txt',
                              'data/de.txt',
                              'data/de.txt',
                              'data/google-10000-english.txt',
                              'data/google-10000-english.txt',
                              'data/google-10000-english.txt',
                              'data/google-10000-english.txt']}

install_requires = \
['python-telegram-bot>=13.4.1,<14.0.0']

setup_kwargs = {
    'name': 'angelsaechsisch-telegram',
    'version': '0.1.3',
    'description': "Ein wundervoller Telegram Roboter, der dich höflich daran erinnert kein Angelsächsisch zu nutzen. Nach dem Vorbild des besten Unter's dieser Erde: r/ich_iel",
    'long_description': "# Ein Nachrichtenraum-Roboter, der Angelsächsisch rügt \n\nEin wundervoller Telegram Roboter, der euch in jeder Gruppenunterhaltung auf Telegram höflich daran erinnert kein Angelsächsisch zu nutzen. Nach dem Vorbild des besten Unter's dieser Erde: [r/ich_iel](https://www.reddit.com/r/ich_iel/)\n\n![](./bilder/gruppengespräch.png)\n\n## Wie füge ich den Roboter zu meiner Gruppenunterhaltung hinzu?\n\nDer Gruppenunterhaltungs-Administrator muss den Roboter hinzufügen. Dabei geht man genauso vor, als würde man einen normalen Nutzer der Gruppe hinzufügen:\n\n**Gruppen-Einstellungen -> Person hinzufügen -> Suche nach** `angelsaechsisch_telegram_bot`\n\nEventuell muss man noch explizit erlauben, dass der Roboter die Nachrichten lesen darf. Falls du dabei bedenken hast, bitte Kapitel [Datenschutz](#datenschutz) durchlesen.\n\n## Befehle\n\n**`/start` und `/hilfe`**\n\nMit diesen Befehlen wird eine Übersicht gezeigt. In dieser sind alle Befehle sowie die aktuellen Einstellungen gelistet.\n\n**`/amtag X`**\n\nMit diesem Befehl kann eingestellt werden, wie oft euch der Roboter **pro Tag** daran erinnert kein Angelsächsisch zu nutzen. Um Mitternacht setzt sich der Zähler zurück. `X` muss dabei ganzzahlig und >= 0 sein.\n\n**`/warte X`**\n\nMit diesem Befehl kann eingestellt werden, wie viele Minuten zwischen zwei Erinnerungen mindestens vergehen soll. `X` muss dabei ganzzahlig und >= 0 sein.\n\n**`/ausnahme XYZ`**\n\nFalls der Roboter mal ein Wort als Angelsächsisch interpretiert, dass aber eigentlich in Ordnung ist, kann dieses Wort über `/ausnahme WORT` zu einer Ausnahmeliste hinzugefügt werden. Das Wort wird in Zukunft nicht mehr als Angelsächsisch erkannt.\n\n**`/nullen`**\n\nMit diesem Befehl werden die täglichen Zähler (vergangene Zeit seit der letzten Nachricht und Anzahl der am Tag bereits versandten Nachrichten) zurückgesetzt.\n\n## Datenschutz\n\nDamit der Roboter euch höflich daran erinnern kann Angelsächsisch zu nutzen, **muss er die Nachrichten natürlich lesen**. Ich verspreche hoch und heilig, keinen Schabernack mit den Daten zu treiben. Wenn du allerdings Bedenken hast, kannst du den Roboter auch einfach selber ausführen und deiner Gruppe bereitstellen. Mehr dazu in [diesem Kapitel.](#eigene-installation)\n\n## Eigene Installation\n\nFalls du den Roboter selber ausführen möchtest, kannst du das gerne tun. Dazu bitte wie folgt vorgehen:\n\n1. Der Roboter ist auf Ubuntu 20.10 entwickelt und getestet und sollte somit auf jeder Linux Distribution mit Python >= 3.8 laufen (Niedriger wahrscheinlich auch, aber nicht getestet). Er kann einfach über\n\n    ```shell\n    pip install angelsaechsisch-telegram\n    ```\n\n    installiert werden.\n    \n2. Außerdem muss ein neuer Roboter bei Telegram angelegt werden, das geht aber sehr einfach. **[Hier](https://sendpulse.com/knowledge-base/chatbot/create-telegram-chatbot) gibt's eine einfache Anleitung dazu**. Wichtig ist noch, dass ihr dem Roboter Gruppenrechte und Leserechte gebt. Das geht im BotFather Chat wie folgt:\n\n   - **mybots -> ROBOTER-NAME -> Bot Settings -> Allow Groups -> Turn groups on**\n\n   - **mybots -> ROBOTER-NAME -> Bot Settings -> Group Privacy -> Turn off**\n\n3. Der BotFather hat dir einen TOKEN ausgespuckt, mit dem du den Roboter ausführen kannst:\n   \n   ```shell\n   python3 -m angelsaechsisch_telegram TOKEN\n   ```\n\n4. Der Roboter sollte jetzt laufen. Über `/start` lässt sich das Menü aufrufen.\n\n5. TODO ~~Damit der Roboter auch bei OS-Neustart oder nach einem Absturz wieder loslegt, sollte das Programm noch durch systemd überwacht werden.~~\n## Quellen\n\n- [Deutsches Wörterbuch](https://raw.githubusercontent.com/creativecouple/all-the-german-words/master/corpus/de.txt)\n\n- [Angelsächsisches Wörterbuch](https://github.com/first20hours/google-10000-english/blob/master/google-10000-english.txt)\n",
    'author': 'leuchtum',
    'author_email': 'acct.d-mueller@mailbox.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
