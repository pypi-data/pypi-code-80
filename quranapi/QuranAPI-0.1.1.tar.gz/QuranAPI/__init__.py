import discord
import asyncio
import aiohttp

async def get_verse(verse_id, language, channel):
  chapter = int(verse_id.split(':')[0])
  verse = int(verse_id.split(':')[1])
  if language == "english":
    async with aiohttp.ClientSession() as cs:
      async with cs.get(f"http://quranapi.azurewebsites.net/api/verse/?chapter={chapter}&number={verse}&lang=en") as r:
        res = await r.json()
        embed = discord.Embed(
          color = discord.Color.purple()
        )
        embed.set_author(name=res["ChapterName"])
        embed.add_field(name="Verse:", value=res["Text"])
        embed.set_footer(text="Powered by QuranAPI")
        await channel.send(embed=embed)
  if language == "arabic":
    async with aiohttp.ClientSession() as cs:
      async with cs.get(f"http://quranapi.azurewebsites.net/api/verse/?chapter={chapter}&number={verse}") as r:
        res = await r.json()
        embed = discord.Embed(
        color = discord.Color.purple()
        )
        embed.set_author(name=res["ChapterName"])
        embed.add_field(name="Verse:", value=res["Text"])
        embed.set_footer(text="Powered by QuranAPI")
        await channel.send(embed=embed)
        
async def random_verse(language, channel):
  if language == "english":
    async with aiohttp.ClientSession() as cs:
      async with cs.get("http://quranapi.azurewebsites.net/api/verse/?lang=en") as r:
        res = await r.json()
        embed = discord.Embed(
          color = discord.Color.purple()
        )
        embed.set_author(name=res["ChapterName"])
        embed.add_field(name="Verse:", value=res["Text"])
        embed.set_footer(text="Powered by QuranAPI")
        await channel.send(embed=embed)
  if language == "arabic":
    async with aiohttp.ClientSession() as cs:
      async with cs.get("http://quranapi.azurewebsites.net/api/verse/") as r:
        res = await r.json()
        embed = discord.Embed(
          color = discord.Color.purple()
        )
        embed.set_author(name=res["ChapterName"])
        embed.add_field(name="Verse:", value=res["Text"])
        embed.set_footer(text="Powered by QuranAPI")
        await channel.send(embed=embed)

headers = {'content-type': 'application/json'}

async def prayer_times(address, channel):
  async with aiohttp.ClientSession() as cs:
    async with cs.get(f"http://api.aladhan.com/v1/timingsByAddress?address={address}", headers=headers) as r:
      res = await r.json()
      fajr = res["data"]["timings"]["Fajr"]
      sunrise = res["data"]["timings"]["Sunrise"]
      dhuhr = res['data']['timings']['Dhuhr']
      asr = res['data']['timings']['Asr']
      maghrib = res['data']['timings']['Maghrib']
      isha = res['data']['timings']['Isha']
      imsak = res['data']['timings']['Imsak']
      midnight = res['data']['timings']['Midnight']
      date = res['data']['date']['readable']
      embed = discord.Embed(
        color = discord.Color.purple()
      )
      embed.set_author(name=f"Prayertimes for {address}")
      embed.add_field(name="Date", value=f"{date}")
      embed.add_field(name="Imsak", value=f"{imsak}")
      embed.add_field(name="Fajr", value=f"{fajr}")
      embed.add_field(name="Sunrise", value=f"{sunrise}")
      embed.add_field(name="Dhuhr", value=f"{dhuhr}")
      embed.add_field(name="Asr", value=f"{asr}")
      embed.add_field(name="Maghrib", value=f"{maghrib}")
      embed.add_field(name="Isha", value=f"{isha}")
      embed.add_field(name="Midnight", value=f"{midnight}")
      embed.set_footer(text="Powered by QuranAPI")
      await channel.send(embed=embed)
  
      