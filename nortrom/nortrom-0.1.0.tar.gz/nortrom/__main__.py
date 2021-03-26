import typing as t
import discord as d
import discord.ext as de
import discord.ext.commands as dec
import discord_slash as ds
import os
import logging
logging.basicConfig(level="DEBUG")


# TODO: restrict intents
bot = dec.Bot(command_prefix="!", intents=d.Intents.default())
sbot = ds.SlashCommand(client=bot, sync_commands=False)


@sbot.slash(name="mute", description="Mute all members in the voice channel you're in.", guild_ids=[176353500710699008])
async def _mute(ctx: ds.SlashContext):
    voice: t.Optional[d.VoiceState] = ctx.author.voice
    if voice is None:
        await ctx.send(content="⚠️ You're not in a voice channel.", hidden=True)
        return

    channel: d.VoiceChannel = voice.channel
    members: list[d.Member] = channel.members
    for member in members:
        await member.edit(mute=True)

    await ctx.send(content="🔇 Speak not.")


@sbot.slash(name="unmute", description="Unmute all members in the voice channel you're in.", guild_ids=[176353500710699008])
async def _unmute(ctx: ds.SlashContext):
    voice: t.Optional[d.VoiceState] = ctx.author.voice
    if voice is None:
        await ctx.send(content="⚠️ You're not in a voice channel.", hidden=True)
        return

    channel: d.VoiceChannel = voice.channel
    members: list[d.Member] = channel.members
    for member in members:
        await member.edit(mute=False)

    await ctx.send(content="🔊 Speak your last.")


@sbot.slash(name="deafen", description="Deafen all members in the voice channel you're in.", guild_ids=[176353500710699008])
async def _deafen(ctx: ds.SlashContext):
    voice: t.Optional[d.VoiceState] = ctx.author.voice
    if voice is None:
        await ctx.send(content="⚠️ You're not in a voice channel.", hidden=True)
        return

    channel: d.VoiceChannel = voice.channel
    members: list[d.Member] = channel.members
    for member in members:
        await member.edit(deafen=True)

    await ctx.send(content="🔇 Hear not.")


@sbot.slash(name="undeafen", description="Undeafen all members in the voice channel you're in.", guild_ids=[176353500710699008])
async def _undeafen(ctx: ds.SlashContext):
    voice: t.Optional[d.VoiceState] = ctx.author.voice
    if voice is None:
        await ctx.send(content="⚠️ You're not in a voice channel.", hidden=True)
        return

    channel: d.VoiceChannel = voice.channel
    members: list[d.Member] = channel.members
    for member in members:
        await member.edit(deafen=False)

    await ctx.send(content="🔊 You haven't heard the last of me.")


print("Running bot...")
bot.run(os.environ["DISCORD_BOT_TOKEN"])
