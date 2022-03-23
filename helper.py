from typing import Callable

from discord import Role, Message
from discord_slash import SlashContext

from config import *


def isGameRole(role: Role) -> bool:
    return str(role.colour) == str(COLOUR)


async def log(message: str) -> None:
    print(message)


async def executeRoleCommand(ctx: SlashContext, role: Role, f: Callable[[SlashContext, Role], None],
                             successMessage: str, invalidRoleMessage: str):
    try:
        if not isGameRole(role):
            if invalidRoleMessage != None and len(invalidRoleMessage) > 0:
                await ctx.send(invalidRoleMessage)
        else:
            await f(ctx, role)
            if successMessage != None and len(successMessage) > 0:
                await ctx.send(successMessage)
    except Exception as e:
        await ctx.send("An error occured")
        await log(f"An error occured when {ctx.author.mention} attempted to do something with {role.mention}: {e}")


def messageHasGif(message: Message):
    if "tenor.com/view" in message.content or "giphy.com/media" in message.content or ".gif" in message.content:
        return True
    if message.attachments:
        pass
    # unfinished below here
    gifEmbeds = ["gifv"]
    gifFileTypes = ["gif"]
    gifSites = ["giphy.com/media", "tenor.com/view"]
    return (
            any([embed.type in ["gifv"] or any([site in embed.url for site in gifSites]) for embed in
                 message.embeds]) or
            any([attachment.content_type in gifFileTypes for attachment in message.attachments]) or
            any([any([site in embed.url for site in gifSites]) for embed in message.embeds])
    )


def messageHasDiscordInvite(message: Message):
    return "discord.gg" in message.content.lower() or "discord.com/invite" in message.content.lower()
