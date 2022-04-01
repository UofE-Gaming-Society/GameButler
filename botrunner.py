import sys

from discord import Intents
from discord.ext import commands
from discord_slash import SlashCommand

import config

if __name__ == "__main__":
    bot = commands.Bot(command_prefix='~', intents=Intents.all(), case_insensitive=True)
    slash = SlashCommand(bot, sync_commands=True)

    bot.load_extension("GameButler")
    bot.load_extension("GameRoleManager")
    bot.load_extension("SpamFilter")
    bot.load_extension("MiscCommands")
    bot.load_extension("ErrorHandler")
    bot.load_extension("AprilFools")

    bot.git_update = False
    bot.restart = False

    bot.run(config.TOKEN)

    # return code 0 means neither restart nor update
    # return code 2 means restart without update
    # return code 4 means update without restart
    # return code 6 means update and restart
    sys.exit(bot.restart * 2 + bot.git_update * 4)
