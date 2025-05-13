import discord
from discord.ext import commands
from discord import app_commands

import helper


class ErrorHandler(commands.Cog):
    """Cog for handling errors globally."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Register the error handler for slash commands
        self.bot.tree.on_error = self.on_app_command_error

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        """Handles errors for old-style commands."""
        if isinstance(error, commands.CommandNotFound):
            message = "Command not found."
        elif isinstance(error, commands.CommandOnCooldown):
            message = f"This command is on cooldown. Try again after {round(error.retry_after, 1)} seconds."
        elif isinstance(error, commands.MissingPermissions):
            message = "You do not have the required permissions to use this command."
        elif isinstance(error, commands.MissingRole):
            message = f"You do not have the required role to use this command."
        else:
            await helper.error(str(error), ctx.channel)
            return

        await ctx.send(message)

    async def on_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        """Handles errors for slash commands."""
        if isinstance(error, app_commands.CommandNotFound):
            message = "Command not found."
        elif isinstance(error, app_commands.CommandOnCooldown):
            message = f"This command is on cooldown. Try again after {round(error.retry_after, 1)} seconds."
        elif isinstance(error, app_commands.MissingPermissions):
            message = "You do not have the required permissions to use this command."
        elif isinstance(error, app_commands.MissingRole):
            message = "You do not have the required role to use this command."
        else:
            await helper.error(str(error), interaction.channel)
            await interaction.response.send_message(
                "An unexpected error occurred. The issue has been logged.", ephemeral=True
            )
            return

        await interaction.response.send_message(message, ephemeral=True)


async def setup(bot: commands.Bot):
    """Sets up the ErrorHandler cog."""
    await bot.add_cog(ErrorHandler(bot))
