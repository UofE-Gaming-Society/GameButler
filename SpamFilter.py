import re
from typing import Dict
import discord
from discord import Message, TextChannel, Member, Guild, Role, Interaction
from discord.ext import commands
from discord import app_commands

import config
import helper
import quotes

GIF_SEARCH_PATTERN = re.compile(
    r"[(http(s)?)://(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)\.gif",
    re.IGNORECASE
)


def is_anti_gif_spam_channel(channel: TextChannel) -> bool:
    """Checks if a channel is configured for anti-GIF spam."""
    return channel.id in config.ANTI_GIF_CHANNELS


def message_has_gif(message: Message) -> bool:
    """Checks if a message contains a GIF."""
    content, author, channel, guild = helper.read_message_properties(message)

    if any(pattern.search(content) for pattern in config.ANTI_GIF_PATTERNS):
        return True
    if re.search(GIF_SEARCH_PATTERN, content):
        return True
    for attachment in message.attachments:
        if attachment.content_type == "image/gif":
            return True
    return False


def message_has_discord_invite(message: Message) -> bool:
    """Checks if a message contains a Discord invite link."""
    content, author, channel, guild = helper.read_message_properties(message)
    pattern = re.compile(r"(https?://)?(www\.)?(discord\.(gg|io|me|li)|discordapp\.com/invite)/.+[a-z]")
    return pattern.search(content) is not None


class SpamFilter(commands.Cog):
    """Cog for managing spam filtering."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.anti_gif_spam_count: Dict[int, int] = {}
        self.anti_gif_spam_error_enabled: Dict[int, bool] = {}
        self.censor = config.CENSOR
        self.antispam = config.ANTISPAM
        self.anti_adverts = config.ANTI_ADVERT

        for channel_id in config.ANTI_GIF_CHANNELS:
            self.anti_gif_spam_count[channel_id] = 0
            self.anti_gif_spam_error_enabled[channel_id] = True

    @app_commands.command(name="anti_ad", description="Toggles Discord server invite removal")
    @app_commands.guilds(*[discord.Object(id=guild_id) for guild_id in config.GUILD_IDS])
    @app_commands.checks.has_permissions(manage_messages=True)
    async def anti_ad(self, interaction: Interaction):
        """Toggles the anti-advertisement feature."""
        self.anti_adverts = not self.anti_adverts
        await helper.log(f"Anti Server Invites Toggled to: {self.anti_adverts}")
        await interaction.response.send_message(
            f"Anti Server Invites Toggled to: {self.anti_adverts}", ephemeral=True
        )

    @app_commands.command(name="antispam", description="Toggles GIF antispam")
    @app_commands.guilds(*[discord.Object(id=guild_id) for guild_id in config.GUILD_IDS])
    @app_commands.checks.has_permissions(manage_messages=True)
    async def antispam(self, interaction: Interaction):
        """Toggles the anti-GIF spam feature."""
        self.antispam = not self.antispam
        await helper.log(f"Anti Gifspam Toggled to: {self.antispam}")
        await interaction.response.send_message(
            f"Anti Gifspam Toggled to: {self.antispam}", ephemeral=True
        )

    @app_commands.command(name="gifban", description="Toggles GIF censorship")
    @app_commands.guilds(*[discord.Object(id=guild_id) for guild_id in config.GUILD_IDS])
    @app_commands.checks.has_permissions(manage_messages=True)
    async def gifban(self, interaction: Interaction):
        """Toggles the GIF censorship feature."""
        self.censor = not self.censor
        if self.antispam:
            self.antispam = False
            await interaction.response.send_message(
                "GIF antispam has been disabled.", ephemeral=True
            )
        await helper.log(f"GIF censorship Toggled to: {self.censor}")
        await interaction.response.send_message(
            f"GIF censorship Toggled to: {self.censor}", ephemeral=True
        )

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        """Handles incoming messages for spam filtering."""
        if not isinstance(message.channel, TextChannel):
            return  # Ignore DMs or group chats

        if message.author == self.bot.user:
            return

        await self.discord_invite_filtering(message)
        await self.gif_censorship(message)
        await self.gif_anti_spam(message)

    async def discord_invite_filtering(self, message: Message) -> None:
        """Filters messages containing Discord invite links."""
        content, author, channel, guild = helper.read_message_properties(message)
        if self.anti_adverts and message_has_discord_invite(message):
            await message.delete()
            await helper.log(f"Deleted an advert from {author.mention} in {channel.mention}")

    async def gif_censorship(self, message: Message) -> None:
        """Filters messages containing GIFs."""
        content, author, channel, guild = helper.read_message_properties(message)
        if self.censor and is_anti_gif_spam_channel(channel) and message_has_gif(message):
            await message.delete()
            await channel.send(f"No GIFs in {channel.mention}, {author.mention}")
            await helper.log(f"GIF detected in {channel.name} posted by {author.display_name}")

    async def gif_anti_spam(self, message: Message) -> None:
        """Implements anti-GIF spam logic."""
        content, author, channel, guild = helper.read_message_properties(message)
        if self.antispam and is_anti_gif_spam_channel(channel):
            if message_has_gif(message):
                if self.anti_gif_spam_count[channel.id] > 0:
                    await message.delete()
                    await helper.log(f"GIF Spam detected in {channel.name} posted by {author.display_name}")
                    if self.anti_gif_spam_error_enabled[channel.id]:
                        await channel.send(f"No GIF spam in {channel.mention}, {author.mention}")
                        self.anti_gif_spam_error_enabled[channel.id] = False
                else:
                    self.anti_gif_spam_count[channel.id] = 1
            elif self.anti_gif_spam_count[channel.id] > 0:
                if len(content) >= 4:
                    self.anti_gif_spam_count[channel.id] += 1
                if self.anti_gif_spam_count[channel.id] > config.LIMIT:
                    self.anti_gif_spam_count[channel.id] = 0
                    self.anti_gif_spam_error_enabled[channel.id] = True
            if config.TEST:
                await helper.log(f"{self.anti_gif_spam_count[channel.id]}/{config.LIMIT} in {channel.name}")


async def setup(bot: commands.Bot):
    """Sets up the SpamFilter cog."""
    await bot.add_cog(SpamFilter(bot))
