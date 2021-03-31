try:
  from LEGENDX import xbot
except:
  pass
try:
  from ULTRAX import xbot
except:
  pass
import re
from telethon import Button, events
@xbot.on(events.callbackquery.CallbackQuery(data=re.compile(b'inlinee')))
async def inlineee(event):
  await xbot.edit("working")