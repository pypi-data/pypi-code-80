import re
from .nimply import nimply

RNUM = re.compile(r"^[-+]?\d+$")
RTRU = re.compile(r"\b(?:t|y|1)\b|\b(?:\+|ay|go|on|up)|(?:tru|acc|asc|day|for|hot|inc|joy|new|pos|top|win|yes|dawn|full|safe|grow|high|just|real|some|know|live|love|open|pure|shin|warm|wis[de]|activ|admit|advan|agree|begin|brigh|build|creat|early|enter|float|f(?:i|ou)nd|grant|light|north|prett|prese|publi|start|succe|victr)", re.IGNORECASE)
RFAL = re.compile(r"\b(?:f|n|0)\b|(?:fal|off|dim|end|low|old|back|cold|cool|dark|dead|decr|desc|dirt|down|dull|dusk|exit|late|sink|ugly|absen|botto|close|finis|night|priva|south|wrong)", re.IGNORECASE)
RNEG = re.compile(r"\b(?:-|na|no|un|in|aft|bad|dis|lie|non|ben[dt]|den[iy]|empt|fail|fake|hate|los[es]|stop|decli|defea|destr|never|negat|refus|rejec|forget|shr[iu]nk|against|is.?nt|can.?(?:no)?t)|(?:hind)", re.IGNORECASE)


def parse(s):
  """Converts string to boolean. `📘`_

  - s: a string

  Example:
    >>> parse("1")            == True
    >>> parse("truthy")       == True
    >>> parse("Not Off")      == True
    >>> parse("Not Inactive") == True
    >>> parse("cold")         == False
    >>> parse("inactive")     == False
    >>> parse("Negative Yes") == False
    >>> parse("Negative Aye") == False

  .. _📘:
    https://github.com/python3f/extra-boolean/wiki/parse
  """
  if RNUM.match(s): return int(s) > 0
  t = RTRU.search(s) is not None
  f = RFAL.search(s) is not None
  n = len(RNEG.findall(s)) % 2 == 1
  return nimply(f, t) == n
