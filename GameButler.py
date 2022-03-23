import random
from typing import List, Tuple

from commands import *


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
    async def on_member_join(self, member):
        await helper.log("Recognised that a member called " + member.name + " joined")
        try:
            try:
                role = discord.utils.get(member.guild.roles, id=config.NEWMEMBERROLE)
                await member.add_roles(role)
                await helper.log("Assigned  new member role to " + member.name)
            except:
                await helper.log(f"Unable to assign role {config.NEWMEMBERROLE}")
        except:
            await helper.log(f"Couldn't message {member.name}")

    # Chat Watch
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        author: discord.Member = message.author
        content: str = message.content

        if type(message.channel) != discord.TextChannel:
            return  # doesn't reply to DMs or group chats
        else:
            channel: discord.TextChannel = message.channel
            guild: discord.Guild = channel.guild

        if author == self.bot.user:
            return

        if (author.id == 381756083028361220) and (channel.id == 369207326101602304):
            await channel.send(f"Moderation Rating: {random.randint(1, 9)}/10")

        await self.iHaveReadTheRules(content, channel, author, guild)
        await self.discordInviteFiltering(message, author, channel)
        await self.gifCensorship(message, author, channel)
        await self.gifAntiSpam(message, author, channel)
        await self.quotes(message, author, channel)

    async def iHaveReadTheRules(self, content: str, channel: discord.TextChannel,
                                author: discord.Member, guild: discord.Guild) -> None:
        if channel.id == config.RULES:
            if "i have read the rules" in content.lower():
                try:
                    role: discord.Role = guild.get_role(config.MEMBERROLE)
                    await author.add_roles(role)
                    await helper.log("Assigned member role to " + author.name)
                    try:
                        newRole: discord.Role = discord.utils.get(author.guild.roles, id=config.NEWMEMBERROLE)
                        await author.remove_roles(newRole)
                    except:
                        await helper.log("Unable to remove role")

                    channel = discord.utils.get(author.guild.channels, id=config.CHANNEL)
                    await channel.send("Welcome " + author.mention + " to the server!!!")
                    await channel.send("Bot help command is ~help, feel free to use it in <#" + str(
                        config.BOTCHANNEL) + "> to add yourself to game roles so you can get notified")
                    await channel.send("React to the relevant messages in <#" + str(
                        config.ROLECHANNEL) + "> to give yourself access to various channels on the server")
                    await helper.log("Sent message about " + author.name)
                except:
                    await helper.log("Unable to assign role")

    async def discordInviteFiltering(self, message: discord.Message,
                                     author: discord.Member, channel: discord.TextChannel) -> None:
        if self.antiAdverts and helper.messageHasDiscordInvite(message):
            await message.delete()
            await helper.log(f"Deleted a advert from {author.mention} in {channel.mention}")

    async def gifCensorship(self, message: discord.Message,
                            author: discord.Member, channel: discord.TextChannel) -> None:
        # Tenor Gif Censorship, allows link embeds but removes all gifs from channel decided in config
        # Toggleable in config
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

    async def gifAntiSpam(self, message: discord.Message, author: discord.Member, channel: discord.TextChannel) -> None:
        # Gif antispam - Toggleable in config

        content: str = message.content
        if channel.id == config.GIF and self.antispam:
            if self.antiGifSpamCount == 0:
                if helper.messageHasGif(message):
                    self.antiGifSpamCount = 1
                elif message.attachments != []:
                    for attachment in message.attachments:
                        if ".gif" in attachment.filename:
                            self.antiGifSpamCount = 1
            else:
                if helper.messageHasGif(message):
                    if self.antiGifSpamCount >= config.LIMIT:
                        self.antiGifSpamCount = 1
                        self.sendErrorMessage = True
                    elif self.sendErrorMessage:
                        await message.delete()
                        await channel.send(
                            "No Gif spam in %s %s " % (channel.mention, author.mention))
                        await helper.log(
                            "Gif Spam detected in %s posted by %s" % (channel.name, author))
                        self.sendErrorMessage = False
                    else:
                        await message.delete()
                        await helper.log(
                            "Gif Spam detected in %s posted by %s" % (channel.name, author))

                elif message.attachments != []:
                    for attachment in message.attachments:
                        if ".gif" in attachment.filename:
                            if self.antiGifSpamCount >= config.LIMIT:
                                self.antiGifSpamCount = 1
                                self.sendErrorMessage = True
                            elif self.sendErrorMessage:
                                await message.delete()
                                await channel.send(
                                    "No Gif spam in %s %s " % (channel.mention, author.mention))
                                await helper.log(
                                    "Gif Spam detected in %s posted by %s" % (channel.name, author))
                                self.sendErrorMessage = False
                            else:
                                await message.delete()
                                await helper.log(
                                    "Gif Spam detected in %s posted by %s" % (channel.name, author))
                elif len(content) >= 4:
                    self.antiGifSpamCount += 1

    async def quotes(self, message: discord.Message, author: discord.Member, channel: discord.TextChannel) -> None:
        content: str = message.content

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
            ("awooga", quotes.copypasta1)
        ]

        for (trigger, response) in mappings:
            if content.lower() == trigger:
                await message.reply(response)
                break
