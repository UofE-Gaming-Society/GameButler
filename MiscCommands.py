from discord.ext import commands
from discord import app_commands
import discord

import config
import quotes


class MiscCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="vgmg", description="Display VGMG rules")
    @app_commands.guilds(*[discord.Object(id=guild_id) for guild_id in config.GUILD_IDS])
    async def vgmg(self, interaction: discord.Interaction):
        """Sends the VGMG rules."""
        await interaction.response.send_message(quotes.vgmgRules)

    @app_commands.command(name="insult", description="Receive an insult from GLADoS")
    @app_commands.guilds(*[discord.Object(id=guild_id) for guild_id in config.GUILD_IDS])
    async def insult(self, interaction: discord.Interaction):
        """Sends a random insult from GLADoS."""
        await interaction.response.send_message(quotes.insult_quote())


# Asynchronous setup function for cog loading
async def setup(bot: commands.Bot):
    await bot.add_cog(MiscCommands(bot))
