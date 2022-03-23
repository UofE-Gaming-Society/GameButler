from typing import Tuple

import discord
from discord import Message


async def log(message: str) -> None:
    print(message)


def read_message_properties(message: Message) -> Tuple[str, discord.Member, discord.TextChannel, discord.Guild]:
    content: str = message.content
    author: discord.Member = message.author
    channel: discord.TextChannel = message.channel
    guild: discord.Guild = message.guild
    return content, author, channel, guild
