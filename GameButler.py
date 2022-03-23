import random
import subprocess

from commands import *


class GameButler(commands.Cog):
    gifspam = 0
    censor = config.CENSOR
    antispam = config.ANTISPAM
    antiads = False
    sendErrorMessage = True

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None

    # Sets bot activity and posts bot name and id.
    @commands.Cog.listener()
    async def on_ready(self):
        await helper.log('Logged in as')
        await helper.log(self.bot.user.name)
        await helper.log(self.bot.user.id)
        await helper.log('------')
        activities = ['World Domination', 'The Matrix', 'Adventure Time', '💯', 'Dying Inside', 'Poggers',
                      'Ping @TTChowder']
        await self.bot.change_presence(activity=discord.Game(name=random.choice(activities)))

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
        channel: discord.TextChannel = message.channel
        author: discord.Member = message.author
        content: str = message.content
        guild: discord.Guild = message.guild

        if author == self.bot.user:
            return

        if (author.id == 381756083028361220) and (channel.id == 369207326101602304):
            await channel.send(f"Moderation Rating: {random.randint(0, 9)}/10")

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

        if self.antiads and helper.messageHasDiscordInvite(message):
            await message.delete()

        if content == '99':
            response = random.choice(quotes.brooklyn_99_quotes)
            await channel.send(response)

        if content.lower() == 'glados':
            response = "```" + random.choice(quotes.glados_quotes) + "```"
            await channel.send(response)

        if content.lower() == 'lemons':
            response = "```" + random.choice(quotes.lemon_quotes) + "```"
            await channel.send(response)

        if 'if life gives you lemons' in content.lower():
            response = quotes.lemonade
            await channel.send(response)

        # Read Fortune - Requires fortune and cowsay
        if content.lower() == "fortune":
            fortune = subprocess.check_output('fortune | cowsay', shell=True, universal_newlines=True)
            await channel.send("```{}```".format(fortune))

        if content.lower() == "moo":
            moo = subprocess.check_output('cowsay "Have you moo\'d today?"', shell=True, universal_newlines=True)
            await channel.send("```{}```".format(moo))

        if content.lower() == "meeba" or content.lower() == "misha":
            await channel.send("<:misha:694298077565026396>")

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

        # Pays Respects
        if content.lower() == 'f':
            await channel.send(author.mention + ' sends their respects')

        if content.lower() == 'awooga':
            await channel.send("{}".format(quotes.copypasta1))

        # Gif antispam - Toggleable in config
        if channel.id == config.GIF and self.antispam:
            if self.gifspam == 0:
                if helper.messageHasGif(message):
                    self.gifspam = 1
                elif message.attachments != []:
                    for attachment in message.attachments:
                        if ".gif" in attachment.filename:
                            self.gifspam = 1
            else:
                if helper.messageHasGif(message):
                    if self.gifspam >= config.LIMIT:
                        self.gifspam = 1
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
                            if self.gifspam >= config.LIMIT:
                                self.gifspam = 1
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
                    self.gifspam += 1

        # await self.bot.process_commands(message)
