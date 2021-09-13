import discord
import asyncio
import random
import subprocess

from discord.ext import commands
from config import *


copypasta1 = """*jaw drops to floor, eyes pop out of sockets accompanied by trumpets, heart beats out of chest, awooga awooga sound effect, pulls chain on train whistle that has appeared next to head as steam blows out, slams fists on table, rattling any plates, bowls or silverware, whistles loudly, fireworks shoot from top of head, pants loudly as tongue hangs out of mouth, wipes comically large bead of sweat from forehead, clears throat, straightens tie, combs hair* Ahem, you look very lovely."""
vgmgrules = """**-Rules-**  

1. Each song has 2 points attached to it. Guessing the song title gives you 1 point, and guessing the game title gives you 1 point.

2. 0.5 points will be given for partial guesses. 

3. Search engines are not allowed. Hints will be given half way through the song.

4. Only Western localised titles accepted. No unofficial translations. 

5. Punctuation such as full stops, colons, etc... in titles do not matter.

6. You can use abbreviations or shortenings for game titles as long as they are recognizable.

7. Please try to guess the entire title, including its number in the series if it is part of one.

8. All decisions are subject to committee discretion.

9. Submit your final answers in a text document to a committee member or helper when the game is over and it will be marked!!"""

lemonade ="""
```All right, I've been thinking. When life gives you lemons? Don't make lemonade. 
Make life take the lemons back! Get mad! 'I don't want your damn lemons! What am I supposed to do with these?`
Demand to see life's manager! Make life rue the day it thought it could give Gurg lemons! Do you know who I am? 
I'm the man who's going to burn your house down! With the lemons! 
I'm going to get my engineers to invent a combustible lemon that burns your house down!```"""

intents = discord.Intents.all()


bot = commands.Bot(command_prefix='~', intents=intents, case_insensitive = True)
bot.gifspam = 0
bot.censor = CENSOR
bot.antispam = ANTISPAM
bot.antiads = False
bot.sendErrorMessage = True




#Bot Commands

#~help gives outline of all main commands

#vgmg rules command
@bot.command(name="vgmg", help = "print vgmg rules")
async def vgmg(ctx):
    await ctx.send(vgmgrules)

#list role command
@bot.command(name = "listroles", help = "get all game roles")
async def listroles(ctx):
    roles = []
    for role in ctx.guild.roles:
        if str(role.colour) == str(COLOUR):
            roles.append("{0.name}".format(role))
    await ctx.send(', '.join(roles))

#Join role command
@bot.command(name = "join",usage = "role", help = """Join game role, Multi worded roles require " " """)
async def join(ctx, arg):
    member = ctx.message.author
    try:
        role = discord.utils.get(member.guild.roles, name=arg.lower())
        if str(role.colour) != str(COLOUR):
           await ctx.send("This role is not a valid game role")
           print(role.colour)
           print(COLOUR)
        else:
            try:
                await member.add_roles(role)
                await ctx.send("Role assigned")
            except:
                await ctx.send("Role does not exist")
    except:
        await ctx.send("Role does not exist")
        
#Leave role command
@bot.command(name = "leave",usage = "role", help = """leave game role, Multi worded roles require " " """)
async def leave(ctx, arg):
    member = ctx.message.author
    try:
        role = discord.utils.get(member.guild.roles, name=arg.lower())
        if str(role.colour) != str(COLOUR):
           await ctx.send("This role is not a valid game role")
           print(role.colour)
           print(COLOUR)
        else: 
            try:
                await member.remove_roles(role)
                await ctx.send("Left Role")
            except:
                await ctx.send("You do not have this role")
    except:
        await ctx.send("Role does not exist")

#Create role command
@bot.command(name = "create", usage = "role", help = """Create game role - Must have Manage role Permission, Multi worded roles require " """)
@commands.has_permissions(manage_roles=True)
async def create(ctx, arg):
    try:
        guild = ctx.guild
        await guild.create_role(name=arg.lower(),colour=discord.Colour(HEXCOLOUR),mentionable = True)
        await ctx.send("Role created")
    except:
        await ctx.send("Insufficient Permissions")

#Delete role command
@bot.command(name = "delete", usage = "role", help = """Delete game role - Must have Manage role Permission, Multi worded roles require " " """)
@commands.has_permissions(manage_roles=True)
async def delete(ctx, arg):
    try:
        guild = ctx.guild
        role = discord.utils.get(guild.roles, name=arg.lower())
        if str(role.colour) != str(COLOUR):
           await ctx.send("This role is not a valid game role")
           print(role.colour)
           print(COLOUR)
        else: 
            try:
                await role.delete()
                await ctx.send("Role Deleted")
            except:
                await ctx.send("You do not have this role")
    except:
        await ctx.send("Role does not exist or Insufficient Permissions")

#list role member command
@bot.command(name = "list", usage = "role", help = """list all members in game role, Multi worded roles require " " """)
async def list(ctx, arg):
    try:
        role = discord.utils.get(ctx.guild.roles, name=arg.lower())
        if str(role.colour) != str(COLOUR):
           await ctx.send("This role is not a valid game role")
           print(role.colour)
           print(COLOUR)
        else:
            try:
                members =[]
                empty = True
                for member in ctx.message.guild.members:
                    if role in member.roles:
                        members.append("{0.name}".format(member))
                        empty = members == []
                if empty:
                    await ctx.send("Nobody has the role {}".format(role.mention))
                await ctx.send(', '.join(members))
            except:
                await ctx.send("Role does not exist")
    except:
        await ctx.send("Role does not exist")

@bot.command(name = "anti_ad",help = "Toggles discord server invite removal")
@commands.has_permissions(manage_messages=True)
async def anti_ad(ctx):
    bot.antiads = not bot.antiads
    print (bot.antiads)
    await ctx.send("Anti Server Invites Toggled to: " + str(bot.antiads))

@bot.command(name = "antispam",help = "Toggles gif antispam")
@commands.has_permissions(manage_messages=True)
async def antispam(ctx):
    bot.antispam = not bot.antispam
    print (bot.antispam)
    await ctx.send("Gifspam Toggled to: " + str(bot.antispam))

@bot.command(name = "gifban",help = "Toggles gif censorship")
@commands.has_permissions(manage_messages=True)
async def gifban(ctx):
    bot.censor = not bot.censor
    if bot.antispam:
        bot.antispam = not bot.antispam
        await ctx.send("Gif antispam has been disabled")
    print (bot.censor)
    await ctx.send("Gif censorship Toggled to: " + str(bot.censor))
  
#Sets bot activity and posts bot name and id.
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    activities = ['World Domination', 'The Matrix', 'Adventure Time', '💯', 'Dying Inside', 'Poggers', 'All hail creator Chowder']
    await bot.change_presence(activity=discord.Game(name=random.choice(activities)))

#Welcomes new member in channel decided in config and assigns welcome role also in config
@bot.event
async def on_member_join(member):
    print("Recognised that a member called " + member.name + " joined")
    try:
        try:
            role = discord.utils.get(member.guild.roles, id=NEWMEMBERROLE)
            await member.add_roles(role)
            print("Assigned  new member role to " + member.name)
        except:
            print("Unable to assign role" + role)
    except:
        print("Couldn't message " + member.name)


                                
#Chat Watch
@bot.event
async def on_message(message):
    #stops jeeves responding to itself
    if message.author == bot.user:
        return

    if message.channel.id == RULES:
        if "i have read the rules" in message.content.lower():
            member = message.author
            try:
                role = discord.utils.get(member.guild.roles, id=MEMBERROLE)
                await member.add_roles(role)
                print("Assigned role to " + member.name)
                try:
                    newrole = discord.utils.get(member.guild.roles, id=NEWMEMBERROLE)
                    await member.remove_roles(newrole)
                except:
                    print("Unable to remove role")

                channel = discord.utils.get(message.author.guild.channels, id = CHANNEL)
                await channel.send("Welcome " + message.author.mention + " to the server!!!")
                await channel.send("Bot help command is ~help, feel free to use it in <#" + str(BOTCHANNEL) + "> to add yourself to game roles so you can get notified")
                await channel.send("React to the relevent messages in <#" + str(ROLECHANNEL) + "> to give yourself access to various channels on the server")
                print("Sent message about " + message.author.name)
            except:
                print("Unable to assign role")
            

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
    if ("tenor.com/view" in message.content or "giphy.com/media" in message.content or ".gif" in message.content) and bot.censor:
        if message.channel.id == GIF:
            await message.delete()
            await message.channel.send("No Gifs in %s %s " % (bot.get_channel(GIF).mention, message.author.mention))
            print ("Gif detected in %s posted by %s" % (bot.get_channel(GIF),message.author))
    elif message.attachments != [] and bot.censor:
        for attachment in message.attachments:
            if ".gif" in attachment.filename:
                await message.delete()
                await message.channel.send("No Gifs in %s %s " % (bot.get_channel(GIF).mention, message.author.mention))
                print ("Gif detected in %s posted by %s" % (bot.get_channel(GIF),message.author))

    #Pays Respects    
    if message.content.lower() == 'f':
        await message.channel.send(message.author.mention + ' sends their respects')

    if message.content.lower() == 'awooga':
        await message.channel.send("{}".format(copypasta1))

    #Gif antispam - Toggleable in config
    if message.channel.id == GIF and bot.antispam:
        if bot.gifspam == 0:
            if "tenor.com/view" in message.content or "giphy.com/media" in message.content or ".gif" in message.content:
                bot.gifspam = 1
            elif message.attachments != []:
                for attachment in message.attachments:
                    if ".gif" in attachment.filename:
                        bot.gifspam = 1
        else:
            if "tenor.com/view" in message.content or "giphy.com/media" in message.content or ".gif" in message.content:
                if bot.gifspam >= LIMIT:
                    bot.gifspam = 1
                    bot.sendErrorMessage = True
                elif bot.sendErrorMessage:
                    await message.delete()
                    await message.channel.send("No Gif spam in %s %s " % (bot.get_channel(GIF).mention, message.author.mention))
                    print ("Gif Spam detected in %s posted by %s" % (bot.get_channel(GIF),message.author))
                    bot.sendErrorMessage = False
                else:
                    await message.delete()
                    print ("Gif Spam detected in %s posted by %s" % (bot.get_channel(GIF),message.author))
                    
            elif message.attachments != []:
                for attachment in message.attachments:
                    if ".gif" in attachment.filename:
                        if bot.gifspam >= LIMIT:
                            bot.gifspam = 1
                            bot.sendErrorMessage = True
                        elif bot.sendErrorMessage:
                            await message.delete()
                            await message.channel.send("No Gif spam in %s %s " % (bot.get_channel(GIF).mention, message.author.mention))
                            print ("Gif Spam detected in %s posted by %s" % (bot.get_channel(GIF),message.author))
                            bot.sendErrorMessage = False
                        else:
                            await message.delete()
                            print ("Gif Spam detected in %s posted by %s" % (bot.get_channel(GIF),message.author))
            elif len(message.content) >= 4:
                bot.gifspam += 1
  
    await bot.process_commands(message)



   
bot.run(TOKEN)
