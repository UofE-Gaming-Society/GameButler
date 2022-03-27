from discord.ext import commands
from discord_slash import cog_ext, SlashContext

import config
import quotes


class MiscCommands(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # vgmg rules command
    @cog_ext.cog_slash(name="vgmg", description="Display VGMG rules", guild_ids=config.GUILD_IDS)
    async def vgmg(self, ctx: SlashContext):
        await ctx.send(quotes.vgmgRules)

    # GLADoS insult
    @cog_ext.cog_slash(
        name="insult",
        description="Receive an insult from GLADoS",
        guild_ids=config.GUILD_IDS,
        options=[]
    )
    async def insult(self, ctx: SlashContext):
        await ctx.reply(quotes.insult_quote())


def setup(bot: commands.Bot):
    bot.add_cog(MiscCommands(bot))
