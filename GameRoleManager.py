from typing import Callable, Awaitable

import discord
from discord import Role, Interaction
from discord.ext import commands
from discord import app_commands

import config
import helper


def is_game_role(role: Role) -> bool:
    """Checks if a role is a game role based on its color."""
    return role.colour.value == config.HEXCOLOUR


async def execute_game_role_command(
    interaction: Interaction,
    role: Role,
    f: Callable[[Interaction, Role], Awaitable[None]],
    success_message: str,
    invalid_role_message: str
) -> bool:
    """Executes a function on a game role."""
    try:
        if not is_game_role(role):
            if invalid_role_message:
                await interaction.response.send_message(invalid_role_message, ephemeral=True)
        else:
            await f(interaction, role)
            if success_message:
                await interaction.response.send_message(success_message, ephemeral=True)
                return True
    except Exception as e:
        await helper.error(
            f"An error occurred when {interaction.user.mention} executed a command on {role.mention}: {e}",
            interaction.channel
        )
    return False


async def list_members_with_role(interaction: Interaction, role: Role) -> None:
    """Lists all members with a specific role."""
    members = [member.display_name for member in role.members]
    if not members:
        await interaction.response.send_message(f"Nobody has the role {role.mention}", ephemeral=True)
    else:
        await interaction.response.send_message(
            f"Members with the {role.name} role: " + ', '.join(members),
            ephemeral=True
        )


class GameRoleManager(commands.Cog):
    """Cog for managing game roles."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Build a hashmap of game roles at startup: {role_id: role_object}
        self.game_roles = {}
        self._build_game_roles_cache()

    def _build_game_roles_cache(self):
        """Builds the initial cache of game roles."""
        # This should be called after the bot is ready and has access to guilds
        for guild in self.bot.guilds:
            for role in guild.roles:
                if is_game_role(role):
                    self.game_roles[role.id] = role

    def _add_game_role(self, role: Role):
        """Adds a role to the cache if it's a game role."""
        if is_game_role(role):
            self.game_roles[role.id] = role

    def _remove_game_role(self, role: Role):
        """Removes a role from the cache."""
        self.game_roles.pop(role.id, None)

    @commands.Cog.listener()
    async def on_ready(self):
        # Rebuild cache in case roles were not available at __init__
        self._build_game_roles_cache()

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        self._add_game_role(role)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        self._remove_game_role(role)

    @app_commands.command(name="listroles", description="List all game roles")
    @app_commands.guilds(*[discord.Object(id=guild_id) for guild_id in config.GUILD_IDS])
    async def listroles(self, interaction: Interaction):
        """Lists all game roles in the server."""
        # Filter roles for this guild only
        roles = [role for role in self.game_roles.values() if role.guild == interaction.guild]
        if not roles:
            await interaction.response.send_message("No game roles found.", ephemeral=True)
            return

        # Pretty print: numbered list with mentions
        pretty = "\n".join(f"{idx+1}. {role.mention}" for idx, role in enumerate(roles))
        await interaction.response.send_message(f"**Game Roles:**\n{pretty}", ephemeral=True)

    @app_commands.command(name="join", description="Join a game role")
    @app_commands.describe(role="The role to join")
    @app_commands.guilds(*[discord.Object(id=guild_id) for guild_id in config.GUILD_IDS])
    async def join(self, interaction: Interaction, role: Role):
        """Allows a user to join a game role."""
        await execute_game_role_command(
            interaction,
            role,
            lambda i, r: i.user.add_roles(r),
            "Role assigned successfully.",
            "This is not a valid game role."
        )

    @app_commands.command(name="leave", description="Leave a game role")
    @app_commands.describe(role="The role to leave")
    @app_commands.guilds(*[discord.Object(id=guild_id) for guild_id in config.GUILD_IDS])
    async def leave(self, interaction: Interaction, role: Role):
        """Allows a user to leave a game role."""
        await execute_game_role_command(
            interaction,
            role,
            lambda i, r: i.user.remove_roles(r),
            "Role removed successfully.",
            "You do not have this role."
        )

    @app_commands.command(name="create", description="Create a new game role")
    @app_commands.describe(role_name="The name of the new game role")
    @app_commands.guilds(*[discord.Object(id=guild_id) for guild_id in config.GUILD_IDS])
    @commands.has_permissions(manage_roles=True)
    async def create(self, interaction: Interaction, role_name: str):
        """Creates a new game role."""
        try:
            role_name = role_name.lower()
            if any(role_name == r.name for r in interaction.guild.roles):
                await interaction.response.send_message(f"{role_name} already exists.", ephemeral=True)
                return

            new_role: Role = await interaction.guild.create_role(
                name=role_name,
                colour=discord.Colour(config.HEXCOLOUR),
                mentionable=True
            )
            self._add_game_role(new_role)
            await interaction.response.send_message(f"{new_role.mention} role created successfully.", ephemeral=True)
            await helper.log(f"{interaction.user.name} created {new_role.name}")
        except discord.Forbidden:
            await interaction.response.send_message("I do not have permission to create roles.", ephemeral=True)
        except Exception as e:
            await helper.error(
                f"An error occurred when {interaction.user.mention} attempted to create a role called {role_name}: {e}",
                interaction.channel
            )

    @app_commands.command(name="delete", description="Delete a game role")
    @app_commands.describe(role="The role to delete")
    @app_commands.guilds(*[discord.Object(id=guild_id) for guild_id in config.GUILD_IDS])
    @commands.has_permissions(manage_roles=True)
    async def delete(self, interaction: Interaction, role: Role):
        """Deletes a game role."""
        role_name = role.name
        if await execute_game_role_command(
            interaction,
            role,
            lambda i, r: r.delete(reason=f"Deleted by {i.user}"),
            "Role deleted successfully.",
            "This is not a valid game role."
        ):
            self._remove_game_role(role)
            await helper.log(f"{interaction.user.name} deleted {role_name}")

    @app_commands.command(name="list", description="List all members in a game role")
    @app_commands.describe(role="The role to list members for")
    @app_commands.guilds(*[discord.Object(id=guild_id) for guild_id in config.GUILD_IDS])
    async def list(self, interaction: Interaction, role: Role):
        """Lists all members in a specific game role."""
        await list_members_with_role(interaction, role)


async def setup(bot: commands.Bot):
    """Sets up the GameRoleManager cog."""
    await bot.add_cog(GameRoleManager(bot))
