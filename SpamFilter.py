import re
from typing import Dict

from discord import Message, TextChannel, Member, Guild, Role
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

import config
import helper
import quotes


def is_anti_gif_spam_channel(channel: TextChannel) -> bool:
    return channel.id in config.ANTI_GIF_CHANNELS


def message_has_gif(message: Message):
    content, author, channel, guild = helper.read_message_properties(message)

    # checks for disallowed gif patterns using regex, defined in config
    if any([pattern.search(content) is not None for pattern in config.ANTI_GIF_PATTERNS]):
        return True
    return False


def message_has_discord_invite(message: Message) -> bool:
    # uses regex to test for whether a message has a discord invite link in it
    content, author, channel, guild = helper.read_message_properties(message)
    pattern = re.compile(r"(https?://)?(www\.)?(discord\.(gg|io|me|li)|discordapp\.com/invite)/.+[a-z]")
    return pattern.search(content) is not None


class SpamFilter(commands.Cog):
    anti_gif_spam_count: Dict[int, int] = {}
    anti_gif_spam_error_enabled: Dict[int, bool] = {}
    censor = config.CENSOR
    antispam = config.ANTISPAM
    anti_adverts = config.ANTI_ADVERT
    sendErrorMessage = True

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        for channelId in config.ANTI_GIF_CHANNELS:
            self.anti_gif_spam_count[channelId] = 0
            self.anti_gif_spam_error_enabled[channelId] = True

    @cog_ext.cog_slash(
        name="anti_ad",
        description="Toggles Discord server invite removal",
        guild_ids=config.GUILD_IDS
    )
    @commands.has_permissions(manage_messages=True)
    async def anti_ad(self, ctx: SlashContext):
        self.anti_adverts = not self.anti_adverts
        await helper.log(f"Anti Server Invites Toggled to: {self.anti_adverts}")
        await ctx.send(f"Anti Server Invites Toggled to: {self.anti_adverts}")

    @cog_ext.cog_slash(
        name="antispam",
        description="Toggles gif antispam",
        guild_ids=config.GUILD_IDS
    )
    @commands.has_permissions(manage_messages=True)
    async def antispam(self, ctx: SlashContext):
        self.antispam = not self.antispam
        await helper.log(f"Anti Gifspam Toggled to: {self.antispam}")
        await ctx.send(f"Anti Gifspam Toggled to: {self.antispam}")

    @cog_ext.cog_slash(
        name="gifban",
        description="Toggles gif censorship",
        guild_ids=config.GUILD_IDS
    )
    @commands.has_permissions(manage_messages=True)
    async def gifban(self, ctx: SlashContext):
        self.censor = not self.censor
        if self.antispam:
            self.antispam = not self.antispam
            await ctx.send("Gif antispam has been disabled")
        await helper.log(f"Gif censorship Toggled to: {self.censor}")
        await ctx.send(f"Gif censorship Toggled to: {self.censor}")

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if type(message.channel) != TextChannel:
            return  # doesn't reply to DMs or group chats

        if message.author == self.bot.user:
            return

        await self.i_have_read_the_rules(message)
        await self.discord_invite_filtering(message)
        await self.gif_censorship(message)
        await self.gif_anti_spam(message)

    async def discord_invite_filtering(self, message: Message) -> None:
        content, author, channel, guild = helper.read_message_properties(message)
        if self.anti_adverts and message_has_discord_invite(message):
            await message.delete()
            await helper.log(f"Deleted a advert from {author.mention} in {channel.mention}")

    async def gif_censorship(self, message: Message) -> None:
        # Tenor Gif Censorship, allows link embeds but removes all gifs from channel decided in config
        # Toggleable in config
        content, author, channel, guild = helper.read_message_properties(message)
        if self.censor and is_anti_gif_spam_channel(channel) and message_has_gif(message):
            await message.delete()
            await channel.send("No Gifs in %s %s " % (channel.mention, author.mention))
            await helper.log("Gif detected in %s posted by %s" % (channel.name, author.display_name))

    async def gif_anti_spam(self, message: Message) -> None:
        # Gif antispam - Toggleable in config
        content, author, channel, guild = helper.read_message_properties(message)
        if self.antispam and is_anti_gif_spam_channel(channel):
            # only continue if antispam is enabled and this message was sent in an anti gif spam channel
            if message_has_gif(message):
                if self.anti_gif_spam_count[channel.id] == 0:
                    # gif allowed
                    if author.id == 815956660996276224:
                        break
                    self.anti_gif_spam_count[channel.id] = 1
                else:
                    # gif not allowed
                    await message.delete()
                    await helper.log(f"Gif Spam detected in {channel.name} posted by {author.display_name}")
                    if self.anti_gif_spam_error_enabled[channel.id]:
                        # only shows error message once
                        await channel.send(f"No Gif spam in {channel.mention} {author.mention}")
                        self.anti_gif_spam_error_enabled[channel.id] = False
            else:
                if len(content) >= 4:
                    # message long enough to increment counter towards unlock limit
                    self.anti_gif_spam_count[channel.id] += 1
                if self.anti_gif_spam_count[channel.id] > config.LIMIT:
                    # unlock limit reached, allow another gif
                    self.anti_gif_spam_count[channel.id] = 0
                    self.anti_gif_spam_error_enabled[channel.id] = True
            if config.TEST:
                await helper.log(f"{self.anti_gif_spam_count[channel.id]}/{config.LIMIT} in {channel.name}")

    # Welcomes new member in channel decided in config and assigns welcome role also in config
    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        await helper.log("Recognised that a member called " + member.name + " joined")
        try:
            try:
                guild: Guild = member.guild
                new_member_role: Role = guild.get_role(config.NEWMEMBERROLE)
                await member.add_roles(new_member_role)
                await helper.log(f"Assigned new member role to {member.name}")
            except:
                await helper.log(f"Unable to assign new member role to {member.name}")
        except:
            await helper.log(f"Couldn't message {member.name}")

    async def i_have_read_the_rules(self, message: Message) -> None:
        content, author, channel, guild = helper.read_message_properties(message)
        member_role: Role = guild.get_role(config.MEMBERROLE)
        new_member_role: Role = guild.get_role(config.NEWMEMBERROLE)
        intro_channel = guild.get_channel(config.CHANNEL)
        if channel.id == config.RULES and "i have read the rules" in content.lower() and new_member_role in author.roles:
            await author.add_roles(member_role)
            await author.remove_roles(new_member_role)
            await intro_channel.send(quotes.introduction(author.mention))
            await helper.log(f"Assigned member role to and introduced {author.name}")


def setup(bot: commands.Bot):
    bot.add_cog(SpamFilter(bot))
