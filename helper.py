import discord
import discord_slash
from discord import Role
from discord_slash import SlashContext, SlashCommand, manage_commands

from config import *

from typing import Callable

def isGameRole(role: Role) -> bool:
    return str(role.colour) == str(COLOUR)

async def executeRoleCommand(ctx: SlashContext, role: Role, f: Callable[[SlashContext, Role], None], successMessage: str, invalidRoleMessage: str):
    try:
        if not isGameRole(role):
            if invalidRoleMessage != None and len(invalidRoleMessage) > 0:
                await ctx.send(invalidRoleMessage)
            print("Attempted to add role", role.name, "but", role.colour, "did not match", COLOUR)
        else:
            await f(ctx, role)
            if successMessage != None and len(successMessage) > 0:
                await ctx.send(successMessage)
    except:
        await ctx.send("Role does not exist")