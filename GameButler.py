import asyncio
import random
import subprocess

import os
from dotenv import load_dotenv

import discord
from discord.ext import commands
import discord_slash
from discord_slash import SlashContext, SlashCommand, manage_commands

from config import *
from helper import *
from quotes import *
from commands import *


intents = discord.Intents.all()

import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='~', intents=intents, case_insensitive = True)


bot.gifspam = 0
bot.censor = CENSOR
bot.antispam = ANTISPAM
bot.antiads = False
bot.sendErrorMessage = True

setupBotCommands(bot)

#Sets bot activity and posts bot name and id.
@bot.event
async def on_ready():
    await log('Logged in as')
    await log(bot.user.name)
    await log(bot.user.id)
    await log('------')
    activities = ['World Domination', 'The Matrix', 'Adventure Time', '💯', 'Dying Inside', 'Poggers', 'Ping @TTChowder']
    await bot.change_presence(activity=discord.Game(name=random.choice(activities)))

#Welcomes new member in channel decided in config and assigns welcome role also in config
@bot.event
async def on_member_join(member):
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
@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
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
            

    #funny test function - quote b99
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    if (bot.antiads == True) and ("discord.gg" in message.content.lower() or "discord.com/invite" in message.content.lower()):
        await message.delete()

    if message.content == '99':
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)

    glados_quotes = ["Oh... It's you.","It's been fun. Don't come back.",
    "This next test involves turrets. You remember them, right? They're the pale spherical things that are full of bullets. Oh wait. That's you in five seconds.",
    """
    Momentum; a function of mass and velocity; is conserved between portals.
    In layman's terms: speedy thing goes in, speedy thing comes out.""",
    "Did you know you can donate one or all of your vital organs to the Edinburgh Gamesoc Self-Esteem Fund for Girls? It's true!",
    "Remember, the Edinburgh Gamesoc \"Bring Your Daughter to Work Day\" is the perfect time to have her tested.",
    "How are you holding up? BECAUSE I'M A POTATO.",
    "I think we can put our differences behind us. For science. You monster.",
    "Let's get mad! If we're going to explode, let's at least explode with some dignity.",
    "Although the euthanizing process is remarkably painful, eight out of ten Edinburgh Gamesoc Moderators believe that the Companion Cube is most likely incapable of feeling much pain."
    ]

    lemon_quotes = ["Welcome, gentlemen, to Edinburgh Gamesoc. V-Tubers, Memers, Gamers--you're here because we want the best, and you are it. So: Who is ready to play some games?",
    "Now, you already met one another on the limo ride over, so let me introduce myself. I'm Gurg. I own the place.",
    "They say great gaming is built on the shoulders of giants. Not here. At Gamesoc, we do all our gaming from level 1. No hand holding."
    ]
    
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
    if messageHasGif(message) and bot.censor:
        if message.channel.id == GIF:
                await message.delete()
                await message.channel.send("No Gifs in %s %s " % (bot.get_channel(GIF).mention, message.author.mention))
                await log ("Gif detected in %s posted by %s" % (bot.get_channel(GIF),message.author))
    elif message.attachments != [] and bot.censor:
        for attachment in message.attachments:
            if ".gif" in attachment.filename:
                await message.delete()
                await message.channel.send("No Gifs in %s %s " % (bot.get_channel(GIF).mention, message.author.mention))
                await log ("Gif detected in %s posted by %s" % (bot.get_channel(GIF),message.author))

    #Pays Respects    
    if message.content.lower() == 'f':
        await message.channel.send(message.author.mention + ' sends their respects')

    if message.content.lower() == 'awooga':
        await message.channel.send("{}".format(copypasta1))

    #Gif antispam - Toggleable in config
    if message.channel.id == GIF and bot.antispam:
        if bot.gifspam == 0:
            if messageHasGif(message):
                bot.gifspam = 1
            elif message.attachments != []:
                for attachment in message.attachments:
                    if ".gif" in attachment.filename:
                        bot.gifspam = 1
        else:
            if messageHasGif(message):
                if bot.gifspam >= LIMIT:
                    bot.gifspam = 1
                    bot.sendErrorMessage = True
                elif bot.sendErrorMessage:
                    await message.delete()
                    await message.channel.send("No Gif spam in %s %s " % (bot.get_channel(GIF).mention, message.author.mention))
                    await log ("Gif Spam detected in %s posted by %s" % (bot.get_channel(GIF),message.author))
                    bot.sendErrorMessage = False
                else:
                    await message.delete()
                    await log ("Gif Spam detected in %s posted by %s" % (bot.get_channel(GIF),message.author))
                    
            elif message.attachments != []:
                for attachment in message.attachments:
                    if ".gif" in attachment.filename:
                        if bot.gifspam >= LIMIT:
                            bot.gifspam = 1
                            bot.sendErrorMessage = True
                        elif bot.sendErrorMessage:
                            await message.delete()
                            await message.channel.send("No Gif spam in %s %s " % (bot.get_channel(GIF).mention, message.author.mention))
                            await log ("Gif Spam detected in %s posted by %s" % (bot.get_channel(GIF),message.author))
                            bot.sendErrorMessage = False
                        else:
                            await message.delete()
                            await log ("Gif Spam detected in %s posted by %s" % (bot.get_channel(GIF),message.author))
            elif len(message.content) >= 4:
                bot.gifspam += 1
  
    await bot.process_commands(message)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot.run(TOKEN)
