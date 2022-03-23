from discord import Intents
from discord.ext import commands

from GameButler import GameButler
from commands import setupBotCommands
from config import TOKEN

bot = commands.Bot(command_prefix='~', intents=Intents.all(), case_insensitive=True)
bot.add_cog(GameButler(bot))
setupBotCommands(bot)

bot.run(TOKEN)
