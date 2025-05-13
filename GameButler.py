import random
import subprocess
from typing import List, Tuple

import discord
from discord import Message, Interaction
from discord.ext import commands
from discord import app_commands

import config
import helper
import quotes


class GameButler(commands.Cog):
    """Cog for managing bot-wide functionality."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Sets bot activity and logs startup messages."""
        await helper.log(f"Initialising {self.bot.user.name} #{self.bot.user.id}")
        await helper.log(random.choice(quotes.glados_startup))
        await helper.log('------')
        await self.bot.change_presence(activity=discord.Game(name=random.choice(quotes.activities)))
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Ignore messages from bots
        if message.author.bot:
            return

        # Ignore messages in DMs
        if isinstance(message.channel, discord.DMChannel):
            return

        # Define your mappings
        mappings: List[Tuple[str, str]] = [
            ("99", random.choice(quotes.brooklyn_99_quotes)),
            ("glados", f"```{random.choice(quotes.glados_quotes)}```"),
            ("lemons", f"```{random.choice(quotes.lemon_quotes)}```"),
            ("if life gives you lemons", quotes.lemonade),
            ("fortune", f"```{quotes.fortune()}```"),
            ("moo", f"```{quotes.moo()}```"),
            ("f", f"{message.author.mention} sends their respects"),
            ("awooga", quotes.copypasta1),
            ("divide by zero", quotes.error_quote()),
            (f"<@!{self.bot.user.id}>", quotes.insult_quote())
        ]

        trigger_lc = message.content.lower()
        for (key, response) in mappings:
            if trigger_lc == key.lower():
                await message.channel.send(response)
                break

    @app_commands.command(name="restart", description="Restart this bot")
    @app_commands.guilds(*[discord.Object(id=guild_id) for guild_id in config.GUILD_IDS])
    @app_commands.checks.has_role(config.BOT_ADMIN_ROLE)
    async def restart(self, interaction: Interaction):
        """Restarts the bot."""
        self.bot.git_update = False
        self.bot.restart = True
        await interaction.response.send_message("Restarting...", ephemeral=True)
        await self.bot.close()

    @app_commands.command(name="update", description="Update this bot")
    @app_commands.guilds(*[discord.Object(id=guild_id) for guild_id in config.GUILD_IDS])
    @app_commands.checks.has_role(config.BOT_ADMIN_ROLE)
    async def update(self, interaction: Interaction):
        """Updates the bot via git pull and restarts."""
        self.bot.git_update = True
        self.bot.restart = True
        await interaction.response.send_message("Updating...", ephemeral=True)
        await self.bot.close()

    @app_commands.command(name="reload-cog", description="Reload a specific Cog")
    @app_commands.describe(cog="The name of the cog to reload")
    @app_commands.guilds(*[discord.Object(id=guild_id) for guild_id in config.GUILD_IDS])
    @app_commands.checks.has_role(config.BOT_ADMIN_ROLE)
    async def reload_cog(self, interaction: Interaction, cog: str):
        """Reloads a specific cog."""
        try:
            self.bot.reload_extension(cog)
            await helper.log(f"{interaction.user.display_name} reloaded {cog}")
            await interaction.response.send_message(f"Reloaded {cog}", ephemeral=True)
        except commands.errors.ExtensionNotLoaded:
            await interaction.response.send_message(f"Unknown Cog: {cog}", ephemeral=True)

    @app_commands.command(name="sync-commands", description="Force slash command sync")
    @app_commands.guilds(*[discord.Object(id=guild_id) for guild_id in config.GUILD_IDS])
    @app_commands.checks.has_role(config.BOT_ADMIN_ROLE)
    async def sync_commands(self, interaction: Interaction):
        """Forces a sync of all slash commands."""
        await helper.log(f"{interaction.user.display_name} triggered command resync")
        await self.bot.tree.sync()
        await interaction.response.send_message("Re-synced all commands", ephemeral=True)

    @app_commands.command(name="git-pull", description="Perform a git pull")
    @app_commands.guilds(*[discord.Object(id=guild_id) for guild_id in config.GUILD_IDS])
    @app_commands.checks.has_role(config.BOT_ADMIN_ROLE)
    async def git_pull(self, interaction: Interaction):
        """Performs a git pull to update the bot."""
        await helper.log(f"{interaction.user.display_name} began a git pull")
        output = subprocess.Popen("git pull", shell=True, stdout=subprocess.PIPE).communicate()[0]
        await helper.log(str(output.decode("utf-8")))
        await interaction.response.send_message("Git pull completed", ephemeral=True)

    @app_commands.command(name="quote", description="Respond with a random quote")
    @app_commands.describe(trigger="The trigger word for the quote")
    @app_commands.guilds(*[discord.Object(id=guild_id) for guild_id in config.GUILD_IDS])
    async def quote(self, interaction: Interaction, trigger: str):
        """Responds with a random quote based on the trigger."""
        mappings: List[Tuple[str, str]] = [
            ("99", random.choice(quotes.brooklyn_99_quotes)),
            ("glados", f"```{random.choice(quotes.glados_quotes)}```"),
            ("lemons", f"```{random.choice(quotes.lemon_quotes)}```"),
            ("if life gives you lemons", quotes.lemonade),
            ("fortune", f"```{quotes.fortune()}```"),
            ("moo", f"```{quotes.moo()}```"),
            ("f", f"{interaction.user.mention} sends their respects"),
            ("awooga", quotes.copypasta1),
            ("divide by zero", quotes.error_quote()),
            (f"<@!{self.bot.user.id}>", quotes.insult_quote())
        ]

        trigger_lc = trigger.lower()
        for (key, response) in mappings:
            if trigger_lc == key.lower():
                await interaction.response.send_message(response, ephemeral=True)
                return

        await interaction.response.send_message("No matching quote found.", ephemeral=True)

    @app_commands.command(name="report", description="Report an incident")
    @app_commands.describe(user="The user being reported", explanation="Explanation of the incident")
    @app_commands.guilds(*[discord.Object(id=guild_id) for guild_id in config.GUILD_IDS])
    async def report(self, interaction: Interaction, user: str, explanation: str):
        """Allows users to report incidents."""
        ticket_channel = self.bot.get_channel(config.TICKET_CHANNEL)
        if ticket_channel:
            await ticket_channel.send(
                f"A report was made against {user} with an explanation of: {explanation}. "
                f"<@&{config.COMMITTEE_ROLE}> <@&{config.MODERATOR_ROLE}>"
            )
            await interaction.response.send_message(
                "Your report has been sent to moderators and committee. We hope to talk to you soon! ❤️",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "Unable to send the report. Please contact a moderator directly.", ephemeral=True
            )


async def setup(bot: commands.Bot):
    """Sets up the GameButler cog."""
    await bot.add_cog(GameButler(bot))
