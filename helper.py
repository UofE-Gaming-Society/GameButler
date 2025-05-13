import datetime
from typing import Tuple

import discord
from discord import Message


import quotes


async def log(message: str) -> None:
    """Logs a message with a timestamp."""
    print(f"{datetime.datetime.now()}: {message}")


async def error(message: str, channel: discord.abc.Messageable) -> None:
    """Logs an error and sends an error quote to the specified channel."""
    await log(message)
    await channel.send(quotes.error_quote())


def read_message_properties(message: Message) -> Tuple[str, discord.Member, discord.TextChannel, discord.Guild]:
    """
    Extracts and returns the content, author, channel, and guild from a Discord message.

    Args:
        message (Message): The Discord message object.

    Returns:
        Tuple[str, discord.Member, discord.TextChannel, discord.Guild]: A tuple containing the message content,
        author, channel, and guild.
    """
    content: str = message.content
    author: discord.Member = message.author
    channel: discord.TextChannel = message.channel
    guild: discord.Guild = message.guild
    return content, author, channel, guild
