from typing import List, Callable

from discord import Message, TextChannel, Member, Guild, Role
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

import config
import helper
import quotes


class SpamFilter(commands.Cog):
    antiGifSpamCount = 0
    censor = config.CENSOR
    antispam = config.ANTISPAM
    antiAdverts = False
    sendErrorMessage = True

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="anti_ad",
        description="Toggles Discord server invite removal",
        guild_ids=config.GUILD_IDS
    )
    @commands.has_permissions(manage_messages=True)
    async def anti_ad(self, ctx: SlashContext):
        self.antiAdverts = not self.antiAdverts
        await helper.log(f"Anti Server Invites Toggled to: {self.antiAdverts}")
        await ctx.send(f"Anti Server Invites Toggled to: {self.antiAdverts}")

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

        processes: List[Callable[[Message], None]] = [
            self.iHaveReadTheRules,
            self.discordInviteFiltering,
            self.gifCensorship,
            self.gifAntiSpam
        ]

        for process in processes:
            await process(message)

    async def discordInviteFiltering(self, message: Message) -> None:
        content, author, channel, guild = helper.readMessageProperties(message)
        if self.antiAdverts and helper.messageHasDiscordInvite(message):
            await message.delete()
            await helper.log(f"Deleted a advert from {author.mention} in {channel.mention}")

    async def gifCensorship(self, message: Message) -> None:
        # Tenor Gif Censorship, allows link embeds but removes all gifs from channel decided in config
        # Toggleable in config
        content, author, channel, guild = helper.readMessageProperties(message)
        if helper.messageHasGif(message) and self.censor:
            if channel.id == config.GIF:
                await message.delete()
                channel: TextChannel = channel
                await channel.send(
                    "No Gifs in %s %s " % (channel.mention, author.mention))
                await helper.log("Gif detected in %s posted by %s" % (channel.name, author.display_name))
        elif message.attachments != [] and self.censor:
            for attachment in message.attachments:
                if ".gif" in attachment.filename:
                    await message.delete()
                    await channel.send(
                        "No Gifs in %s %s " % (channel.mention, author.mention))
                    await helper.log("Gif detected in %s posted by %s" % (channel.name, author.display_name))

    async def gifAntiSpam(self, message: Message) -> None:
        # Gif antispam - Toggleable in config
        content, author, channel, guild = helper.readMessageProperties(message)
        if channel.id == config.GIF and self.antispam:
            if not self.antiGifSpamCount:
                # gif allowed
                self.antiGifSpamCount: int = helper.messageHasGif(message)
            else:
                # gif not allowed
                if helper.messageHasGif(message):
                    if self.antiGifSpamCount >= config.LIMIT:
                        self.antiGifSpamCount = 1
                        self.sendErrorMessage = True
                    else:
                        await message.delete()
                        await helper.log(f"Gif Spam detected in {channel.name} posted by {author.display_name}")
                        if self.sendErrorMessage:
                            # only shows error message once
                            await channel.send(f"No Gif spam in {channel.mention} {author.mention}")
                            self.sendErrorMessage = False
                elif len(content) >= 4:
                    self.antiGifSpamCount += 1

    # Welcomes new member in channel decided in config and assigns welcome role also in config
    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        await helper.log("Recognised that a member called " + member.name + " joined")
        try:
            try:
                guild: Guild = member.guild
                newMemberRole: Role = guild.get_role(config.NEWMEMBERROLE)
                await member.add_roles(newMemberRole)
                await helper.log(f"Assigned new member role to {member.name}")
            except:
                await helper.log(f"Unable to assign new member role to {member.name}")
        except:
            await helper.log(f"Couldn't message {member.name}")

    async def iHaveReadTheRules(self, message: Message) -> None:
        content, author, channel, guild = helper.readMessageProperties(message)
        if channel.id == config.RULES:
            if "i have read the rules" in content.lower():
                try:
                    memberRole: Role = guild.get_role(config.MEMBERROLE)
                    await author.add_roles(memberRole)
                    await helper.log(f"Assigned member role to {author.name}")
                    try:
                        newMemberRole: Role = guild.get_role(config.NEWMEMBERROLE)
                        await author.remove_roles(newMemberRole)
                    except:
                        await helper.log(f"Unable to remove new member role from {author.display_name}")

                    introChannel = guild.get_channel(config.CHANNEL)
                    await introChannel.send(quotes.introduction(author.mention))
                    await helper.log(f"Introduced {author.name}")
                except:
                    await helper.log("Unable to assign role")
