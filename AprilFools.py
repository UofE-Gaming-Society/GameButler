import random
from typing import Dict

import aiohttp
from discord import Interaction
from discord import Webhook, AsyncWebhookAdapter
from discord.ext import commands
from discord import app_commands

import config


class AprilFools(commands.Cog):
    """Cog for handling April Fools' Day events."""
    karma_scores: Dict[str, int] = {}

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def starting_karma(self) -> int:
        """Generates a random starting karma value."""
        return random.randint(1, random.randint(1, 100))

    async def send_webhook_message(self, content: str, username: str, avatar_url: str = None):
        """Sends a message to the configured webhook."""
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(config.BALLS_WEBHOOK, adapter=AsyncWebhookAdapter(session))
            await webhook.send(content, username=username, avatar_url=avatar_url)

    @app_commands.command(name="karma", description="Check or modify karma for a user")
    @app_commands.describe(user="The user whose karma to check or modify", action="Add or subtract karma", reason="Reason for the karma change")
    async def karma(self, interaction: Interaction, user: str, action: str, reason: str = "No reason provided"):
        """Handles karma modifications."""
        if action not in ["++", "--"]:
            await interaction.response.send_message("Invalid action. Use `++` to add or `--` to subtract karma.", ephemeral=True)
            return

        if user not in self.karma_scores:
            self.karma_scores[user] = self.starting_karma()

        if action == "++":
            self.karma_scores[user] += 1
        elif action == "--":
            self.karma_scores[user] -= 1

        karma_message = f"{user} now has {self.karma_scores[user]} karma. Reason: {reason}"
        await self.send_webhook_message(karma_message, username="KarmaBot")
        await interaction.response.send_message(karma_message, ephemeral=True)

    @app_commands.command(name="randomize", description="Randomly modify a message for April Fools")
    @app_commands.describe(message="The message to randomize")
    async def randomize(self, interaction: Interaction, message: str):
        """Randomly modifies a message for April Fools."""
        random_int = random.randint(0, 100)

        if random_int < 5:
            # Send the original message to the webhook
            await self.send_webhook_message(message, username=interaction.user.name, avatar_url=interaction.user.avatar.url)
            await interaction.response.send_message("Message sent to the webhook!", ephemeral=True)
        elif 47 <= random_int <= 50:
            # Replace a random word with "butt"
            message_split = message.split(" ")
            random_word = random.randint(0, len(message_split) - 1)
            message_split[random_word] = "butt"
            modified_message = " ".join(message_split)
            await self.send_webhook_message(modified_message, username="ButtBot")
            await interaction.response.send_message("Message modified and sent to the webhook!", ephemeral=True)
        else:
            await interaction.response.send_message("No modifications were made to the message.", ephemeral=True)


async def setup(bot: commands.Bot):
    """Sets up the AprilFools cog."""
    await bot.add_cog(AprilFools(bot))
