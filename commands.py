import os
from dotenv import load_dotenv

import discord
from discord.ext import commands
import discord_slash
from discord_slash import SlashContext, SlashCommand, manage_commands

from config import *
from helper import *
from quotes import *


intents = discord.Intents.all()

bot = commands.Bot(command_prefix='~', intents=intents, case_insensitive = True)
slash = SlashCommand(bot, sync_commands=True)

bot.gifspam = 0
bot.censor = CENSOR
bot.antispam = ANTISPAM
bot.antiads = False
bot.sendErrorMessage = True


def setupBotCommands(bot: commands.Bot):
    slash = SlashCommand(bot, sync_commands=True)

    #vgmg rules command
    @slash.slash(name="vgmg", description="Display VGMG rules", guild_ids=[GUILD_ID])
    async def vgmg(ctx):
        await ctx.send(vgmgrules)

    #list role command
    @slash.slash(name="listroles", description="get all game rolls", guild_ids=[GUILD_ID])
    async def listroles(ctx: SlashContext):
        roles = [ "{0.name}".format(role) for role in ctx.guild.roles if isGameRole(role) ]
        await ctx.send(', '.join(roles))

    #Join role command
    @slash.slash(
        name = "join",
        description="Join game role",
        options=[
            manage_commands.create_option(
                name="role",
                description="Name of game role",
                option_type=8, # role
                required=True
            )
        ],
        guild_ids=[GUILD_ID]
    )
    async def join(ctx: SlashContext, role: discord.Role):
        await executeRoleCommand(
            ctx,
            role,
            lambda c, r : c.author.add_roles(r),
            "Role assigned",
            "This is not a valid game role"
        )
            
    #Leave role command
    @slash.slash(
        name="leave",
        description="Leave game role",
        options=[
            manage_commands.create_option(
                name="role",
                description="Name of game role",
                option_type=8, # role
                required=True
            )
        ],
        guild_ids=[GUILD_ID]
    )
    async def leave(ctx: SlashContext, role: discord.Role):
        await executeRoleCommand(
            ctx,
            role,
            lambda c, r : c.author.remove_roles(r),
            "Role removed",
            "You do not have this role"
        )

    #Create role command
    @slash.slash(
        name="create",
        description="Create game role - Must have Manage role Permission",
        options=[
            manage_commands.create_option(
                name="role",
                description="Name of game role",
                option_type=3, # string
                required=True
            )
        ],
        guild_ids=[GUILD_ID]
    )
    @commands.has_permissions(manage_roles=True)
    async def create(ctx: SlashContext, role: str):
        role = role.lower()
        try:
            if not ctx.author.guild_permissions.manage_roles:
                await ctx.send("You have insufficient permissions to modify roles")
            else:
                # check if role with same name already exists
                if any([ role == r.name for r in ctx.guild.roles ]):
                    await ctx.send(f"{role} already exists")
                
                newRole: Role = await ctx.guild.create_role(name=role, colour=discord.Colour(HEXCOLOUR), mentionable=True)
                await ctx.send(f"{newRole.mention} role created")
                await log(f"{ctx.author.mention} created {newRole.mention}")
        except:
            await ctx.send("An error occurred")
            await log(f"An error occured when {ctx.author.mention} attempted to create a role called {role}")

    #Delete role command
    @slash.slash(
        name="delete",
        description="Delete game role - Must have Manage role Permission",
        options=[
            manage_commands.create_option(
                name="role",
                description="Name of game role",
                option_type=8, # role
                required=True
            )
        ],
        guild_ids=[GUILD_ID]
    )
    @commands.has_permissions(manage_roles=True)
    async def delete(ctx: SlashContext, role: discord.Role):
        if ctx.author.guild_permissions.manage_roles:
            roleName = role.mention
            await executeRoleCommand(
                ctx,
                role,
                lambda c, r : r.delete(reason=f"Deleted by {c.author}"),
                "Role deleted",
                "This is not a valid game role"
            )
            await log(f"{ctx.author.mention} deleted {roleName}")
        else:
            await ctx.send("You have insufficient permissions")

    #list role member command
    @slash.slash(
        name="list",
        description="List all members in game role",
        options=[
            manage_commands.create_option(
                name="role",
                description="Name of game role",
                option_type=8, # role
                required=True
            )
        ],
        guild_ids=[GUILD_ID]
    )
    async def list(ctx: SlashContext, role: discord.Role):
        async def listMembersWithRole(c: SlashContext, r: discord.Role):
            members = [ member.display_name for member in role.members ]
            if len(members) == 0:
                await c.send(f"Nobody has the role {r.mention}")
            else:
                await c.send(', '.join(members))

        await executeRoleCommand(
            ctx,
            role,
            lambda c, r : listMembersWithRole(c, r),
            "",
            f"Unknown error when attempting to list members with {role.name} role"
        )



    @slash.slash(
        name="anti_ad",
        description="Toggles Discord server invite removal",
        guild_ids=[GUILD_ID]
    )
    @commands.has_permissions(manage_messages=True)
    async def anti_ad(ctx: SlashContext):
        bot.antiads = not bot.antiads
        await log(f"Anti Server Invites Toggled to: {bot.antiads}")
        await ctx.send(f"Anti Server Invites Toggled to: {bot.antiads}")

    @slash.slash(
        name="antispam",
        description="Toggles gif antispam",
        guild_ids=[GUILD_ID]
    )
    @commands.has_permissions(manage_messages=True)
    async def antispam(ctx: SlashContext):
        bot.antispam = not bot.antispam
        await log(f"Anti Gifspam Toggled to: {bot.antispam}")
        await ctx.send(f"Anti Gifspam Toggled to: {bot.antispam}")

    @slash.slash(
        name="gifban",
        description="Toggles gif censorship",
        guild_ids=[GUILD_ID]
    )
    @commands.has_permissions(manage_messages=True)
    async def gifban(ctx: SlashContext):
        bot.censor = not bot.censor
        if bot.antispam:
            bot.antispam = not bot.antispam
            await ctx.send("Gif antispam has been disabled")
        await log(f"Gif censorship Toggled to: {bot.censor}")
        await ctx.send(f"Gif censorship Toggled to: {bot.censor}")
    