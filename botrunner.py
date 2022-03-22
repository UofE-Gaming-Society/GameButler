import os
from dotenv import load_dotenv

from discord import Intents
from discord.ext import commands

from GameButler import GameButler
from commands import setupBotCommands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='~', intents=Intents.all(), case_insensitive=True)
bot.add_cog(GameButler(bot))
setupBotCommands(bot)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot.run(TOKEN)
