import random
from typing import Dict

import aiohttp
from discord import Message
from discord import Webhook, AsyncWebhookAdapter
from discord.ext import commands

import config


class AprilFools(commands.Cog):
    class AprilFools(commands.Cog):
        karma_scores: Dict[str, int] = {}

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author == self.bot.user:
            return

        if config.APRIL_FOOLS and message.channel.id == config.APRIL_FOOLS_GENERAL:
            random_int = random.randint(0, 100)
            no_irc = False
            add_mode = "++" in message.content
            sub_mode = "--" in message.content
            if add_mode != sub_mode:
                if add_mode:
                    user = message.content.split("++")[0]
                else:
                    user = message.content.split("--")[0]

                if "for" in message.content:
                    reason = "for" + "".join(message.content.split("for")[1])
                else:
                    reason = " "

                if user in self.karma_scores:
                    if add_mode:
                        self.karma_scores[user] += 1
                    else:
                        self.karma_scores[user] -= 1
                else:
                    self.karma_scores[user] = self.starting_karma()
                async with aiohttp.ClientSession() as session:
                    webhook_balls = Webhook.from_url(config.BALLS_WEBHOOK, adapter=AsyncWebhookAdapter(session))
                    await webhook_balls.send(f"{user} now has {self.karma_scores[user]} karma {reason}",
                                             username="botbot")
                no_irc = True

            if random_int < 5 and not no_irc:
                async with aiohttp.ClientSession() as session:
                    webhook_balls = Webhook.from_url(config.BALLS_WEBHOOK, adapter=AsyncWebhookAdapter(session))
                    user_name = message.author.name
                    user_picture = message.author.avatar_url
                    await webhook_balls.send(message.content, username=user_name, avatar_url=user_picture)
                    await message.delete()
                return

            if 47 <= random_int <= 50 and not no_irc:
                message_split = message.content.split(" ")
                random_word = random.randint(0, len(message_split) - 1)
                message_split[random_word] = "butt"
                async with aiohttp.ClientSession() as session:
                    webhook_balls = Webhook.from_url(config.BALLS_WEBHOOK, adapter=AsyncWebhookAdapter(session))
                    user_name = message.author.name
                    await webhook_balls.send(" ".join(message_split), username="buttbot")
                return

    def starting_karma(self) -> int:
        return random.randint(1, random.randint(1, 100))


def setup(bot: commands.Bot):
    bot.add_cog(AprilFools(bot))
