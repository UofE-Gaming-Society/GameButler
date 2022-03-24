import random
from typing import List, Tuple

import discord
from discord import Message
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

import config
import helper
import quotes


class GameButler(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Sets bot activity and posts bot name and id.
    @commands.Cog.listener()
    async def on_ready(self):
        await helper.log(f"Initialising {self.bot.user.name} #{self.bot.user.id}")
        await helper.log(random.choice(quotes.glados_startup))
        await helper.log('------')
        await self.bot.change_presence(activity=discord.Game(name=random.choice(quotes.activities)))

    # Chat Watch
    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if type(message.channel) != discord.TextChannel:
            return  # doesn't reply to DMs or group chats

        if message.author == self.bot.user:
            return

        await self.troll(message)
        await self.quotes(message)

    async def troll(self, message: Message) -> None:
        # this is the responsibility of Tom
        content, author, channel, guild = helper.read_message_properties(message)
        if (author.id == 381756083028361220) and (channel.id == 369207326101602304):
            await channel.send(f"Moderation Rating: {random.randint(1, 9)}/10")

        if author.id == 352458055763623947:  # moT
            if random.random() < 0.05:
                await message.delete(delay=300)

    async def quotes(self, message: Message) -> None:
        content, author, channel, guild = helper.read_message_properties(message)

        mappings: List[Tuple[str, str]] = [
            ("99", random.choice(quotes.brooklyn_99_quotes)),
            ("glados", f"```{random.choice(quotes.glados_quotes)}```"),
            ("lemons", f"```{random.choice(quotes.lemon_quotes)}```"),
            ("if life gives you lemons", quotes.lemonade),
            ("fortune", f"```{quotes.fortune()}```"),
            ("moo", f"```{quotes.moo()}```"),
            ("meeba", quotes.misha),
            ("misha", quotes.misha),
            ("f", f"{author.mention} sends their respects"),
            ("awooga", quotes.copypasta1),
            ("divide by zero", quotes.error_quote()),
            (f"<@!{self.bot.user.id}>", quotes.insult_quote())
        ]

        for (trigger, response) in mappings:
            if content.lower() == trigger:
                await message.reply(response)
                break

    @cog_ext.cog_slash(name="close", description="Close this bot", guild_ids=config.GUILD_IDS, options=[])
    async def close(self, ctx: SlashContext):
        self.bot.git_update = False
        self.bot.restart = False
        await ctx.send("Shutting down...")
        await self.bot.close()

    @cog_ext.cog_slash(name="restart", description="Restart this bot", guild_ids=config.GUILD_IDS, options=[])
    async def restart(self, ctx: SlashContext):
        self.bot.git_update = False
        self.bot.restart = True
        await ctx.send("Shutting down...")
        await self.bot.close()

    @cog_ext.cog_slash(name="update", description="Update this bot", guild_ids=config.GUILD_IDS, options=[])
    async def update(self, ctx: SlashContext):
        self.bot.git_update = True
        self.bot.restart = True
        await ctx.send("Shutting down...")
        await self.bot.close()
