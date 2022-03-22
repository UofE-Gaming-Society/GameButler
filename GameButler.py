import asyncio
import random
import subprocess

import discord
from discord.ext import commands
from discord_slash import SlashContext, SlashCommand, manage_commands
import discord_slash

from config import *

from helper import *


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

import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='~', intents=intents, case_insensitive = True)
slash = SlashCommand(bot, sync_commands=True)


bot.gifspam = 0
bot.censor = CENSOR
bot.antispam = ANTISPAM
bot.antiads = False
bot.sendErrorMessage = True


#Bot Commands

#~help gives outline of all main commands

#vgmg rules command
@slash.slash(name="vgmg", description="print VGMG rules", guild_ids=[GUILD_ID])
async def vgmg(ctx):
    await ctx.send(vgmgrules)

#list role command
@slash.slash(name="listroles", description="get all game rolls", guild_ids=[GUILD_ID])
async def listroles(ctx: SlashContext):
    roles = [ "{0.name}".format(role) for role in ctx.guild.roles if isGameRole(role) ]
    await ctx.send(', '.join(roles))

#Join role command
@slash.slash(
    name = "join",
    description="Join game role",
    options=[
        manage_commands.create_option(
            name="role",
            description="Name of game role",
            option_type=8, # role
            required=True
        )
    ],
    guild_ids=[GUILD_ID]
)
async def join(ctx: SlashContext, role: discord.Role):
    await executeRoleCommand(
        ctx,
        role,
        lambda c, r : c.author.add_roles(r),
        "Role assigned",
        "This is not a valid game role"
    )
        
#Leave role command
@slash.slash(
    name="leave",
    description="Leave game role",
    options=[
        manage_commands.create_option(
            name="role",
            description="Name of game role",
            option_type=8, # role
            required=True
        )
    ],
    guild_ids=[GUILD_ID]
)
async def leave(ctx: SlashContext, role: discord.Role):
    await executeRoleCommand(
        ctx,
        role,
        lambda c, r : c.author.remove_roles(r),
        "Role removed",
        "You do not have this role"
    )

#Create role command
@slash.slash(
    name="create",
    description="Create game role - Must have Manage role Permission",
    options=[
        manage_commands.create_option(
            name="role",
            description="Name of game role",
            option_type=3, # string
            required=True
        )
    ],
    guild_ids=[GUILD_ID]
)
@commands.has_permissions(manage_roles=True)
async def create(ctx: SlashContext, role: str):
    role = role.lower()
    try:
        if not ctx.author.guild_permissions.manage_roles:
            await ctx.send("You have insufficient permissions to modify roles")
        else:
            # check if role with same name already exists
            if any([ role == r.name for r in ctx.guild.roles ]):
                await ctx.send(f"{role} already exists")
            
            newRole: Role = await ctx.guild.create_role(name=role, colour=discord.Colour(HEXCOLOUR), mentionable=True)
            await ctx.send(f"{newRole.mention} role created")
            await log(f"{ctx.author.mention} created {newRole.mention}")
    except:
        await ctx.send("An error occurred")
        await log(f"An error occured when {ctx.author.mention} attempted to create a role called {role}")

#Delete role command
@slash.slash(
    name="delete",
    description="Delete game role - Must have Manage role Permission",
    options=[
        manage_commands.create_option(
            name="role",
            description="Name of game role",
            option_type=8, # role
            required=True
        )
    ],
    guild_ids=[GUILD_ID]
)
@commands.has_permissions(manage_roles=True)
async def delete(ctx: SlashContext, role: discord.Role):
    if ctx.author.guild_permissions.manage_roles():
        await executeRoleCommand(
            ctx,
            role,
            lambda c, r : r.delete(f"Deleted by {c.author}"),
            "Role deleted",
            "This is not a valid game role"
        )
    else:
        await ctx.send("You have insufficient permissions")

#list role member command
@slash.slash(
    name="list",
    description="List all members in game role",
    options=[
        manage_commands.create_option(
            name="role",
            description="Name of game role",
            option_type=8, # role
            required=True
        )
    ],
    guild_ids=[GUILD_ID]
)
async def list(ctx: SlashContext, role: discord.Role):
    async def listMembersWithRole(c: SlashContext, r: discord.Role):
        members = [ member.display_name for member in role.members ]
        if len(members) == 0:
            await c.send(f"Nobody has the role {r.mention}")
        else:
            await c.send(', '.join(members))

    await executeRoleCommand(
        ctx,
        role,
        lambda c, r : listMembersWithRole(c, r),
        "",
        f"Unknown error when attempting to list members with {role.name} role"
    )



@slash.slash(
    name="anti_ad",
    description="Toggles Discord server invite removal",
    guild_ids=[GUILD_ID]
)
@commands.has_permissions(manage_messages=True)
async def anti_ad(ctx: SlashContext):
    bot.antiads = not bot.antiads
    print(f"Anti Server Invites Toggled to: {bot.antiads}")
    await ctx.send(f"Anti Server Invites Toggled to: {bot.antiads}")

@slash.slash(
    name="antispam",
    description="Toggles gif antispam",
    guild_ids=[GUILD_ID]
)
@commands.has_permissions(manage_messages=True)
async def antispam(ctx: SlashContext):
    bot.antispam = not bot.antispam
    print(f"Anti Gifspam Toggled to: {bot.antispam}")
    await ctx.send(f"Anti Gifspam Toggled to: {bot.antispam}")

@slash.slash(
    name="gifban",
    description="Toggles gif censorship",
    guild_ids=[GUILD_ID]
)
@commands.has_permissions(manage_messages=True)
async def gifban(ctx: SlashContext):
    bot.censor = not bot.censor
    if bot.antispam:
        bot.antispam = not bot.antispam
        await ctx.send("Gif antispam has been disabled")
    print(f"Gif censorship Toggled to: {bot.censor}")
    await ctx.send(f"Gif censorship Toggled to: {bot.censor}")
  
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
    print("hi")

    #stops jeeves responding to itself
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
