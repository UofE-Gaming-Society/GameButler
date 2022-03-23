from typing import Tuple

import discord
from discord import Message

import quotes


async def log(message: str) -> None:
    print(message)


async def error(message: str, channel: discord.abc.Messageable) -> None:
    await log(message)
    await channel.send(quotes.error_quote())


def read_message_properties(message: Message) -> Tuple[str, discord.Member, discord.TextChannel, discord.Guild]:
    content: str = message.content
    author: discord.Member = message.author
    channel: discord.TextChannel = message.channel
    guild: discord.Guild = message.guild
    return content, author, channel, guild
