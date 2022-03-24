import sys

from discord import Intents
from discord.ext import commands
from discord_slash import SlashCommand

import config
from GameButler import GameButler
from GameRoleManager import GameRoleManager
from MiscCommands import MiscCommands
from SpamFilter import SpamFilter

if __name__ == "__main__":
    bot = commands.Bot(command_prefix='~', intents=Intents.all(), case_insensitive=True)
    slash = SlashCommand(bot, sync_commands=True)

    bot.add_cog(GameButler(bot))
    bot.add_cog(GameRoleManager(bot))
    bot.add_cog(SpamFilter(bot))
    bot.add_cog(MiscCommands(bot))

    bot.git_update = False
    bot.restart = False

    bot.run(config.TOKEN)

    sys.exit(bot.restart * 2 + bot.git_update * 4)
