from discord.ext import commands
from discord_slash import SlashCommand

import config
import quotes


def setupBotCommands(bot: commands.Bot):
    slash = SlashCommand(bot, sync_commands=True)
    butler = bot.get_cog("GameButler")

    # vgmg rules command
    @butler.slash_command(name="vgmg", description="Display VGMG rules", guild_ids=config.GUILD_IDS)
    async def vgmg(ctx):
        await ctx.send(quotes.vgmgRules)
