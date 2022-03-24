import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext, manage_commands

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
        description="Ask GLADoS to insult someone",
        guild_ids=config.GUILD_IDS,
        options=[
            manage_commands.create_option(
                name="target",
                description="Target of GLADoS' impending insult",
                option_type=6,  # user
                required=True
            )
        ]
    )
    async def insult(self, ctx: SlashContext, target: discord.User):
        await ctx.reply(f"{target.mention} {quotes.insult_quote()}")


def setup(bot: commands.Bot):
    bot.add_cog(MiscCommands(bot))
