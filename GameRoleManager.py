from typing import Callable, Awaitable

import discord
from discord import Role
from discord.ext import commands
from discord_slash import cog_ext, SlashContext, manage_commands

import config
import helper


def role_slash_command_option(name="role", description="Name of game role", required=True) -> dict:
    option_type = 8  # role option type
    return manage_commands.create_option(name, description, option_type, required)


def is_game_role(role: Role) -> bool:
    return str(role.colour) == str(config.COLOUR)


async def execute_role_command(ctx: SlashContext, role: Role, f: Callable[[SlashContext, Role], Awaitable[None]],
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
        await helper.error(
            f"An error occurred when {ctx.author.mention} executing a command on {role.mention}: {e}", ctx.channel)


async def list_members_with_role(c: SlashContext, r: Role) -> None:
    members = [member.display_name for member in r.members]
    if len(members) == 0:
        await c.send(f"Nobody has the role {r.mention}")
    else:
        await c.send(f"Members with the {r.name} role: " + ', '.join(members))


class GameRoleManager(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # list role command
    @cog_ext.cog_slash(name="listroles", description="List all game rolls", guild_ids=config.GUILD_IDS)
    async def listroles(self, ctx: SlashContext):
        roles = ["{0.name}".format(role) for role in ctx.guild.roles if is_game_role(role)]
        await ctx.send(', '.join(roles))

    # Join role command
    @cog_ext.cog_slash(
        name="join",
        description="Join game role",
        options=[role_slash_command_option()],
        guild_ids=config.GUILD_IDS
    )
    async def join(self, ctx: SlashContext, role: Role):
        await execute_role_command(
            ctx,
            role,
            lambda c, r: c.author.add_roles(r),
            "Role assigned",
            "This is not a valid game role"
        )

    # Leave role command
    @cog_ext.cog_slash(
        name="leave",
        description="Leave game role",
        options=[role_slash_command_option()],
        guild_ids=config.GUILD_IDS
    )
    async def leave(self, ctx: SlashContext, role: Role):
        await execute_role_command(
            ctx,
            role,
            lambda c, r: c.author.remove_roles(r),
            "Role removed",
            "You do not have this role"
        )

    # Create role command
    @cog_ext.cog_slash(
        name="create",
        description="Create game role - Must have Manage role Permission",
        options=[role_slash_command_option()],
        guild_ids=config.GUILD_IDS
    )
    @commands.has_permissions(manage_roles=True)
    async def create(self, ctx: SlashContext, role: str):
        role = role.lower()
        try:
            if not ctx.author.guild_permissions.manage_roles:
                await ctx.send("You have insufficient permissions to modify roles")
            else:
                # check if role with same name already exists
                if any([role == r.name for r in ctx.guild.roles]):
                    await ctx.send(f"{role} already exists")

                new_role: Role = await ctx.guild.create_role(name=role,
                                                             colour=discord.Colour(config.HEXCOLOUR),
                                                             mentionable=True)
                await ctx.send(f"{new_role.mention} role created")
                await helper.log(f"{ctx.author.mention} created {new_role.mention}")
        except:
            await helper.error(
                f"An error occurred when {ctx.author.mention} attempted to create a role called {role}", ctx.channel)

    # Delete role command
    @cog_ext.cog_slash(
        name="delete",
        description="Delete game role - Must have Manage role Permission",
        options=[role_slash_command_option()],
        guild_ids=config.GUILD_IDS
    )
    @commands.has_permissions(manage_roles=True)
    async def delete(self, ctx: SlashContext, role: Role):
        if ctx.author.guild_permissions.manage_roles:
            role_name = role.mention
            await execute_role_command(
                ctx,
                role,
                lambda c, r: r.delete(reason=f"Deleted by {c.author}"),
                "Role deleted",
                "This is not a valid game role"
            )
            await helper.log(f"{ctx.author.mention} deleted {role_name}")
        else:
            await ctx.send("You have insufficient permissions")

    # list role member command
    @cog_ext.cog_slash(
        name="list",
        description="List all members in game role",
        options=[role_slash_command_option()],
        guild_ids=config.GUILD_IDS
    )
    async def list(self, ctx: SlashContext, role: Role):
        await execute_role_command(
            ctx,
            role,
            lambda c, r: list_members_with_role(c, r),
            "",
            f"Unknown error when attempting to list members with {role.name} role"
        )
