from typing import Callable, Awaitable

import discord
from discord import Role
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

import config
import helper


def is_game_role(role: Role) -> bool:
    return role.colour.value == config.HEXCOLOUR


async def execute_game_role_command(ctx: SlashContext, role: Role, f: Callable[[SlashContext, Role], Awaitable[None]],
                                    success_message: str, invalid_role_message: str) -> bool:
    """Executes a function on a game role. Game roles are defined as rolls with colours matching the config setting.
    The provided function must take SlashContext and Role as arguments in that order.
    Returns True if the command was executed successfully, False otherwise."""
    try:
        if not is_game_role(role):
            if invalid_role_message is not None and len(invalid_role_message) > 0:
                await ctx.send(invalid_role_message)
        else:
            await f(ctx, role)
            if success_message is not None and len(success_message) > 0:
                await ctx.send(success_message)
                return True
    except Exception as e:
        await helper.error(
            f"An error occurred when {ctx.author.mention} executing a command on {role.mention}: {e}", ctx.channel)
    return False


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
        options=[helper.role_slash_command_option()],
        guild_ids=config.GUILD_IDS
    )
    async def join(self, ctx: SlashContext, role: Role):
        await execute_game_role_command(
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
        options=[helper.role_slash_command_option()],
        guild_ids=config.GUILD_IDS
    )
    async def leave(self, ctx: SlashContext, role: Role):
        await execute_game_role_command(
            ctx,
            role,
            lambda c, r: c.author.remove_roles(r),
            "Role removed",
            "You do not have this role"
        )

    # Create role command
    @cog_ext.cog_slash(
        name="create",
        description="Create game role - Must have \"Manage Role\" Permission",
        options=[helper.string_slash_command_option("role", "Name of new game role")],
        guild_ids=config.GUILD_IDS
    )
    @commands.has_permissions(manage_roles=True)
    async def create(self, ctx: SlashContext, role: str):
        try:
            role_name = role.lower()

            # check if role with same name already exists
            if any([role_name == r.name for r in ctx.guild.roles]):
                await ctx.send(f"{role_name} already exists")
                return

            new_role: Role = await ctx.guild.create_role(
                name=role_name,
                colour=discord.Colour(config.HEXCOLOUR),
                mentionable=True
            )
            await ctx.send(f"{new_role.mention} role created")
            await helper.log(f"{ctx.author.name} created {new_role.name}")
        except:
            await helper.error(
                f"An error occurred when {ctx.author.mention} attempted to create a role called {role}", ctx.channel)

    # Delete role command
    @cog_ext.cog_slash(
        name="delete",
        description="Delete game role - Must have Manage role Permission",
        options=[helper.role_slash_command_option()],
        guild_ids=config.GUILD_IDS
    )
    @commands.has_permissions(manage_roles=True)
    async def delete(self, ctx: SlashContext, role: Role):
        if ctx.author.guild_permissions.manage_roles:
            role_name = role.name
            if await execute_game_role_command(
                    ctx,
                    role,
                    lambda c, r: r.delete(reason=f"Deleted by {c.author}"),
                    "Role deleted",
                    "This is not a valid game role"
            ):
                await helper.log(f"{ctx.author.name} deleted {role_name}")
        else:
            await ctx.send("You have insufficient permissions")

    # list role member command
    @cog_ext.cog_slash(
        name="list",
        description="List all members in game role",
        options=[helper.role_slash_command_option()],
        guild_ids=config.GUILD_IDS
    )
    async def list(self, ctx: SlashContext, role: Role):
        await execute_game_role_command(
            ctx,
            role,
            lambda c, r: list_members_with_role(c, r),
            "",
            f"Unknown error when attempting to list members with {role.name} role"
        )


def setup(bot: commands.Bot):
    bot.add_cog(GameRoleManager(bot))
