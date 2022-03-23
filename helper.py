from typing import Callable, Tuple

import discord
from discord import Role, Message
from discord_slash import SlashContext

import config


def is_game_role(role: Role) -> bool:
    return str(role.colour) == str(config.COLOUR)


async def log(message: str) -> None:
    print(message)


async def execute_role_command(ctx: SlashContext, role: Role, f: Callable[[SlashContext, Role], None],
                               success_message: str, invalid_role_message: str):
    try:
        if not is_game_role(role):
            if invalid_role_message is not None and len(invalid_role_message) > 0:
                await ctx.send(invalid_role_message)
        else:
            await f(ctx, role)
            if success_message is not None and len(success_message) > 0:
                await ctx.send(success_message)
    except Exception as e:
        await ctx.send("An error occurred")
        await log(f"An error occurred when {ctx.author.mention} attempted to do something with {role.mention}: {e}")


def message_has_gif(message: Message):
    if "tenor.com/view" in message.content or "giphy.com/media" in message.content or ".gif" in message.content:
        return True
    if message.attachments:
        pass
    # unfinished below here
    gif_embeds = ["gifv"]
    gif_file_types = ["gif"]
    gif_sites = ["giphy.com/media", "tenor.com/view"]
    return (
            any([embed.type in gif_embeds or any([site in embed.url for site in gif_sites]) for embed in
                 message.embeds]) or
            any([attachment.content_type in gif_file_types for attachment in message.attachments]) or
            any([any([site in embed.url for site in gif_sites]) for embed in message.embeds])
    )


def message_has_discord_invite(message: Message):
    return "discord.gg" in message.content.lower() or "discord.com/invite" in message.content.lower()


def read_message_properties(message: Message) -> Tuple[str, discord.Member, discord.TextChannel, discord.Guild]:
    content: str = message.content
    author: discord.Member = message.author
    channel: discord.TextChannel = message.channel
    guild: discord.Guild = message.guild
    return content, author, channel, guild
