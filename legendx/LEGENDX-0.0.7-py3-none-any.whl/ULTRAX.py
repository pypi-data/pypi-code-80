from LEGENDX import xbot
import re
from telethon import Button, events
@xbot.on(events.callbackquery.CallbackQuery(data=re.compile(b'inlinee)))
async def inlineee(event):
  await xbot.edit("working")