from typing import List, Callable

from discord import Message, TextChannel, Member, Guild, Role
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

import config
import helper
import quotes


class SpamFilter(commands.Cog):
    anti_gif_spam_count = 0
    censor = config.CENSOR
    antispam = config.ANTISPAM
    anti_adverts = config.ANTI_ADVERT
    sendErrorMessage = config.PRINT_ERRORS

    def __init__(self, bot: commands.Bot):
        self.bot = bot

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

        processes: List[Callable[[Message], None]] = [
            self.i_have_read_the_rules,
            self.discord_invite_filtering,
            self.gif_censorship,
            self.gif_anti_spam
        ]

        for process in processes:
            await process(message)

    async def discord_invite_filtering(self, message: Message) -> None:
        content, author, channel, guild = helper.read_message_properties(message)
        if self.anti_adverts and helper.message_has_discord_invite(message):
            await message.delete()
            await helper.log(f"Deleted a advert from {author.mention} in {channel.mention}")

    async def gif_censorship(self, message: Message) -> None:
        # Tenor Gif Censorship, allows link embeds but removes all gifs from channel decided in config
        # Toggleable in config
        content, author, channel, guild = helper.read_message_properties(message)
        if helper.message_has_gif(message) and self.censor:
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

    async def gif_anti_spam(self, message: Message) -> None:
        # Gif antispam - Toggleable in config
        content, author, channel, guild = helper.read_message_properties(message)
        if channel.id == config.GIF and self.antispam:
            if not self.anti_gif_spam_count:
                # gif allowed
                self.anti_gif_spam_count: int = helper.message_has_gif(message)
            else:
                # gif not allowed
                if helper.message_has_gif(message):
                    if self.anti_gif_spam_count >= config.LIMIT:
                        self.anti_gif_spam_count = 1
                        self.sendErrorMessage = True
                    else:
                        await message.delete()
                        await helper.log(f"Gif Spam detected in {channel.name} posted by {author.display_name}")
                        if self.sendErrorMessage:
                            # only shows error message once
                            await channel.send(f"No Gif spam in {channel.mention} {author.mention}")
                            self.sendErrorMessage = False
                elif len(content) >= 4:
                    self.anti_gif_spam_count += 1

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
        if channel.id == config.RULES:
            if "i have read the rules" in content.lower():
                try:
                    member_role: Role = guild.get_role(config.MEMBERROLE)
                    await author.add_roles(member_role)
                    await helper.log(f"Assigned member role to {author.name}")
                    try:
                        new_member_role: Role = guild.get_role(config.NEWMEMBERROLE)
                        await author.remove_roles(new_member_role)
                    except:
                        await helper.log(f"Unable to remove new member role from {author.display_name}")

                    intro_channel = guild.get_channel(config.CHANNEL)
                    await intro_channel.send(quotes.introduction(author.mention))
                    await helper.log(f"Introduced {author.name}")
                except:
                    await helper.log("Unable to assign role")
