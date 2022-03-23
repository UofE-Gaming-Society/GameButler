import random
from typing import List, Tuple, Callable

import discord
from discord import Message, Role, Member, Guild
from discord.ext import commands

import config
import helper
import quotes


class GameButler(commands.Cog):
    antiGifSpamCount = 0
    censor = config.CENSOR
    antispam = config.ANTISPAM
    antiAdverts = False
    sendErrorMessage = True

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Sets bot activity and posts bot name and id.
    @commands.Cog.listener()
    async def on_ready(self):
        await helper.log(f"Initialising {self.bot.user.name} #{self.bot.user.id}")
        await helper.log(random.choice(quotes.glados_startup))
        await helper.log('------')
        await self.bot.change_presence(activity=discord.Game(name=random.choice(quotes.activities)))

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

    # Chat Watch
    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if type(message.channel) != discord.TextChannel:
            return  # doesn't reply to DMs or group chats

        if message.author == self.bot.user:
            return

        processes: List[Callable[[Message], None]] = [
            self.iHaveReadTheRules,
            self.discordInviteFiltering,
            self.gifCensorship,
            self.gifAntiSpam,
            self.troll,
            self.quotes
        ]

        for process in processes:
            await process(message)

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
                channel: discord.TextChannel = channel
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

    async def troll(self, message: Message) -> None:
        content, author, channel, guild = helper.readMessageProperties(message)
        if (author.id == 381756083028361220) and (channel.id == 369207326101602304):
            await channel.send(f"Moderation Rating: {random.randint(1, 9)}/10")

    async def quotes(self, message: Message) -> None:
        content, author, channel, guild = helper.readMessageProperties(message)

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
