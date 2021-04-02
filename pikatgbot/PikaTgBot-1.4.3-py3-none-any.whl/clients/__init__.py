from ..core.database import pdb
from ..resources import PikaClient
if pdb.Alpha:
    bot = client = PikaClient(pdb.Alpha)
else:
    bot = client = None

if pdb.Beta:
    bot2 = client2 = PikaClient(pdb.Beta)
else:
    bot2 = client2 = None

if pdb.Gaama:
    bot3 = client3 = PikaClient(pdb.Gaama)
else:
    bot3 = None

if pdb.Delta:
    bot4 = client4 = PikaClient(pdb.Delta)
else:
    bot4 = client4 = None

if pdb.bf_token:
    tgbot = tgbot_client = PikaClient(pdb.Omega, gBot=True)

else:
    tgbot = tgbot_client = None
