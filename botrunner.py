from discord import Intents
from discord.ext import commands
from discord_slash import SlashCommand

from GameButler import GameButler
from GameRoleManager import GameRoleManager
from MiscCommands import MiscCommands
from SpamFilter import SpamFilter
from config import TOKEN

if __name__ == "__main__":
    bot = commands.Bot(command_prefix='~', intents=Intents.all(), case_insensitive=True)
    slash = SlashCommand(bot, sync_commands=True)

    bot.add_cog(GameButler(bot))
    bot.add_cog(GameRoleManager(bot))
    bot.add_cog(SpamFilter(bot))
    bot.add_cog(MiscCommands(bot))

    bot.git_update = False
    bot.restart = False

    try:
        bot.run(TOKEN)
    except Exception as e:
        print("Shutting down...")

    if bot.git_update:
        pass

    if bot.restart:
        pass
