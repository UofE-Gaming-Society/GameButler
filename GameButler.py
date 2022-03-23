import asyncio
import random
import subprocess

import discord
from discord.ext import commands

from config import *
from helper import *
from quotes import *
from commands import *

class GameButler(commands.Cog):

    gifspam = 0
    censor = CENSOR
    antispam = ANTISPAM
    antiads = False
    sendErrorMessage = True

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None

    #Sets bot activity and posts bot name and id.
    @commands.Cog.listener()
    async def on_ready(self):
        await log('Logged in as')
        await log(self.bot.user.name)
        await log(self.bot.user.id)
        await log('------')
        activities = ['World Domination', 'The Matrix', 'Adventure Time', '💯', 'Dying Inside', 'Poggers', 'Ping @TTChowder']
        await self.bot.change_presence(activity=discord.Game(name=random.choice(activities)))

    #Welcomes new member in channel decided in config and assigns welcome role also in config
    @commands.Cog.listener()
    async def on_member_join(self, member):
        await log("Recognised that a member called " + member.name + " joined")
        try:
            try:
                role = discord.utils.get(member.guild.roles, id=NEWMEMBERROLE)
                await member.add_roles(role)
                await log("Assigned  new member role to " + member.name)
            except:
                await log("Unable to assign role" + role)
        except:
            await log("Couldn't message " + member.name)


                                    
    #Chat Watch
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        if (message.author.id == 381756083028361220) and (message.channel.id == 369207326101602304):
            await message.channel.send("Moderation Rating: ", random.randint(0,9), "/10")

        if message.channel.id == RULES:
            if "i have read the rules" in message.content.lower():
                member = message.author
                try:
                    role = discord.utils.get(member.guild.roles, id=MEMBERROLE)
                    await member.add_roles(role)
                    await log("Assigned role to " + member.name)
                    try:
                        newrole = discord.utils.get(member.guild.roles, id=NEWMEMBERROLE)
                        await member.remove_roles(newrole)
                    except:
                        await log("Unable to remove role")

                    channel = discord.utils.get(message.author.guild.channels, id = CHANNEL)
                    await channel.send("Welcome " + message.author.mention + " to the server!!!")
                    await channel.send("Bot help command is ~help, feel free to use it in <#" + str(BOTCHANNEL) + "> to add yourself to game roles so you can get notified")
                    await channel.send("React to the relevent messages in <#" + str(ROLECHANNEL) + "> to give yourself access to various channels on the server")
                    await log("Sent message about " + message.author.name)
                except:
                    await log("Unable to assign role")
                

        if (self.antiads == True) and ("discord.gg" in message.content.lower() or "discord.com/invite" in message.content.lower()):
            await message.delete()

        if message.content == '99':
            response = random.choice(brooklyn_99_quotes)
            await message.channel.send(response)

        if message.content.lower() == 'glados':
            response = "```" + random.choice(glados_quotes) + "```"
            await message.channel.send(response)
        
        if message.content.lower() == 'lemons':
            response = "```" + random.choice(lemon_quotes) + "```"
            await message.channel.send(response)
        
        if 'if life gives you lemons' in message.content.lower():
            response = (lemonade)
            await message.channel.send(response)

        #Read Fortune - Requires fortune and cowsay
        if message.content.lower() == "fortune":
            fortune = subprocess.check_output('fortune | cowsay', shell = True, universal_newlines= True)
            await message.channel.send("```{}```".format(fortune))
        
        if message.content.lower() == "moo":
            moo = subprocess.check_output('cowsay "Have you moo\'d today?"', shell = True, universal_newlines= True)
            await message.channel.send("```{}```".format(moo))

        if message.content.lower() == "meeba" or message.content.lower() == "misha":
            await message.channel.send("<:misha:694298077565026396>")

        #Tenor Gif Censorship, allows link embeds but removes all gifs from channel decided in config
        #Toggleable in config
        if messageHasGif(message) and self.censor:
            if message.channel.id == GIF:
                    await message.delete()
                    await message.channel.send("No Gifs in %s %s " % (self.get_channel(GIF).mention, message.author.mention))
                    await log ("Gif detected in %s posted by %s" % (self.get_channel(GIF),message.author))
        elif message.attachments != [] and self.censor:
            for attachment in message.attachments:
                if ".gif" in attachment.filename:
                    await message.delete()
                    await message.channel.send("No Gifs in %s %s " % (self.get_channel(GIF).mention, message.author.mention))
                    await log ("Gif detected in %s posted by %s" % (self.get_channel(GIF),message.author))

        #Pays Respects    
        if message.content.lower() == 'f':
            await message.channel.send(message.author.mention + ' sends their respects')

        if message.content.lower() == 'awooga':
            await message.channel.send("{}".format(copypasta1))

        #Gif antispam - Toggleable in config
        if message.channel.id == GIF and self.antispam:
            if self.gifspam == 0:
                if messageHasGif(message):
                    self.gifspam = 1
                elif message.attachments != []:
                    for attachment in message.attachments:
                        if ".gif" in attachment.filename:
                            self.gifspam = 1
            else:
                if messageHasGif(message):
                    if self.gifspam >= LIMIT:
                        self.gifspam = 1
                        self.sendErrorMessage = True
                    elif self.sendErrorMessage:
                        await message.delete()
                        await message.channel.send("No Gif spam in %s %s " % (self.get_channel(GIF).mention, message.author.mention))
                        await log ("Gif Spam detected in %s posted by %s" % (self.get_channel(GIF),message.author))
                        self.sendErrorMessage = False
                    else:
                        await message.delete()
                        await log ("Gif Spam detected in %s posted by %s" % (self.get_channel(GIF),message.author))
                        
                elif message.attachments != []:
                    for attachment in message.attachments:
                        if ".gif" in attachment.filename:
                            if self.gifspam >= LIMIT:
                                self.gifspam = 1
                                self.sendErrorMessage = True
                            elif self.sendErrorMessage:
                                await message.delete()
                                await message.channel.send("No Gif spam in %s %s " % (self.get_channel(GIF).mention, message.author.mention))
                                await log ("Gif Spam detected in %s posted by %s" % (self.get_channel(GIF),message.author))
                                self.sendErrorMessage = False
                            else:
                                await message.delete()
                                await log ("Gif Spam detected in %s posted by %s" % (self.get_channel(GIF),message.author))
                elif len(message.content) >= 4:
                    self.gifspam += 1
    
        # await self.bot.process_commands(message)
