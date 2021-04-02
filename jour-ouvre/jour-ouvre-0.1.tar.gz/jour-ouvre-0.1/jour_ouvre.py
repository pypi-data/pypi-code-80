"""JOUR OUVRE."""

import urllib.request
from datetime import date
import sys
import os

__version__ = "0.1"

ICS_URL = (
    "https://etalab.github.io/jours-feries-france-data/ics/jours_feries_metropole.ics"
)

CACHE_FILE = "~/.cache/jours_feries_metropole.ics"


def get_feries():
    """Retourne la liste de jours feries."""
    if not os.path.isfile(CACHE_FILE):
        with urllib.request.urlopen(ICS_URL) as response:  # nosec
            with open(CACHE_FILE, "wb") as file:
                file.write(response.read())

    with open(CACHE_FILE, "r") as file:
        content = file.read()
        return [
            info.replace("DTSTART;VALUE=DATE:", "")
            for info in content.split()
            if "DTSTART" in str(info)
        ]


def is_ferie(feries):
    """Retourne True si aujourd'hui est un jour ferie, False sinon."""
    today = date.today()
    date1 = today.strftime("%Y%m%d")

    return date1 in feries


def is_ouvre(feries):
    """Retourne True si aujourd'hui est un jour ouvre, False sinon."""
    today = date.today()
    date1 = today.strftime("%Y%m%d")

    return not (date1 in feries and today.weekday() in [5, 6])


def main():
    """Methode principale."""
    feries = get_feries()

    if is_ouvre(feries):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
