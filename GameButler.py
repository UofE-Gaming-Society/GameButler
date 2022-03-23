import random
from typing import List, Tuple, Callable

import discord
from discord import Message
from discord.ext import commands

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

        processes: List[Callable[[Message], None]] = [
            self.troll,
            self.quotes
        ]

        for process in processes:
            await process(message)

    async def troll(self, message: Message) -> None:
        content, author, channel, guild = helper.read_message_properties(message)
        if (author.id == 381756083028361220) and (channel.id == 369207326101602304):
            await channel.send(f"Moderation Rating: {random.randint(1, 9)}/10")

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
            ("introduction", quotes.introduction(author.mention))
        ]

        for (trigger, response) in mappings:
            if content.lower() == trigger:
                await message.reply(response)
                break
