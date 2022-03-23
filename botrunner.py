from discord import Intents
from discord.ext import commands
from discord_slash import SlashCommand

from GameButler import GameButler
from GameRoleManager import GameRoleManager
from SpamFilter import SpamFilter
from config import TOKEN

bot = commands.Bot(command_prefix='~', intents=Intents.all(), case_insensitive=True)
slash = SlashCommand(bot)

bot.add_cog(GameButler(bot))
bot.add_cog(GameRoleManager(bot))
bot.add_cog(SpamFilter(bot))

bot.run(TOKEN)
