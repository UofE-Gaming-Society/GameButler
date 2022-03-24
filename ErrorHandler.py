from discord.ext import commands
from discord_slash import SlashContext
from discord_slash.error import SlashCommandError

import helper


class ErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx: SlashContext, error: SlashCommandError):
        if isinstance(error, commands.CommandNotFound):
            message = f"Command not found"
        elif isinstance(error, commands.CommandOnCooldown):
            message = f"This command is on cooldown, try again after {round(error.retry_after, 1)} seconds"
        elif isinstance(error, commands.MissingPermissions):
            message = f"You do not have the required permissions to use this command"
        elif isinstance(error, commands.MissingRole):
            message = f"You do not have the required role to use this command"
        else:
            await helper.error(str(error), ctx.channel)
            return

        await ctx.send(message)


def setup(bot: commands.Bot):
    bot.add_cog(ErrorHandler(bot))
