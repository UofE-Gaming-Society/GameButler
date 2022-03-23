from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

import config
import helper
import quotes


def setupBotCommands(bot: commands.Bot):
    slash = SlashCommand(bot, sync_commands=True)
    butler = bot.get_cog("GameButler")

    # vgmg rules command
    @butler.slash_command(name="vgmg", description="Display VGMG rules", guild_ids=config.GUILD_IDS)
    async def vgmg(ctx):
        await ctx.send(quotes.vgmgRules)

    @butler.slash_command(
        name="anti_ad",
        description="Toggles Discord server invite removal",
        guild_ids=config.GUILD_IDS
    )
    @commands.has_permissions(manage_messages=True)
    async def anti_ad(ctx: SlashContext):
        butler.antiAdverts = not butler.antiAdverts
        await helper.log(f"Anti Server Invites Toggled to: {butler.antiAdverts}")
        await ctx.send(f"Anti Server Invites Toggled to: {butler.antiAdverts}")

    @butler.slash_command(
        name="antispam",
        description="Toggles gif antispam",
        guild_ids=config.GUILD_IDS
    )
    @commands.has_permissions(manage_messages=True)
    async def antispam(ctx: SlashContext):
        butler.antispam = not butler.antispam
        await helper.log(f"Anti Gifspam Toggled to: {butler.antispam}")
        await ctx.send(f"Anti Gifspam Toggled to: {butler.antispam}")

    @butler.slash_command(
        name="gifban",
        description="Toggles gif censorship",
        guild_ids=config.GUILD_IDS
    )
    @commands.has_permissions(manage_messages=True)
    async def gifban(ctx: SlashContext):
        butler.censor = not butler.censor
        if butler.antispam:
            butler.antispam = not butler.antispam
            await ctx.send("Gif antispam has been disabled")
        await helper.log(f"Gif censorship Toggled to: {butler.censor}")
        await ctx.send(f"Gif censorship Toggled to: {butler.censor}")
