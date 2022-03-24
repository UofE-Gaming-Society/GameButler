from typing import Tuple

import discord
from discord import Message
from discord_slash import manage_commands

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


def string_slash_command_option(name: str, description: str, required=True) -> dict:
    option_type = 3  # string option type
    return manage_commands.create_option(name, description, option_type, required)


def role_slash_command_option(name="role", description="Name of game role", required=True) -> dict:
    option_type = 8  # role option type
    return manage_commands.create_option(name, description, option_type, required)
