import discord
import asyncio
import random
from discord.ext import commands
from config import *


intents = discord.Intents.all()

bot = commands.Bot(command_prefix='~', intents=intents, case_insensitive = True)

#Bot Commands

#~help gives outline of all main commands

#Join role command

#list role command
@bot.command(name = "listroles", help = "get all game roles")
async def listroles(ctx):
    roles = []
    for role in ctx.guild.roles:
        if str(role.colour) == str(COLOUR):
            roles.append("{0.name}".format(role))
    await ctx.send(', '.join(roles))


@bot.command(name = "join",usage = "role", help = "Join game role, Multi worded roles require '' ")
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
@bot.command(name = "leave",usage = "role", help = "leave game role")
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
@bot.command(name = "create", usage = "role", help = "Create game role - Must have Manage role Permission")
@commands.has_permissions(manage_roles=True)
async def create(ctx, arg):
    try:
        guild = ctx.guild
        await guild.create_role(name=arg.lower(),colour=discord.Colour(HEXCOLOUR),mentionable = True)
        await ctx.send("Role created")
    except:
        await ctx.send("Insufficient Permissions")

#Delete role command
@bot.command(name = "delete", usage = "role", help = "Delete game role - Must have Manage role Permission")
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
@bot.command(name = "list", usage = "role", help = "list all members in game role")
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



    
    
#Sets bot activity and posts bot name and id.
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    activities = ['World Domination', 'The Matrix', 'Your Mum']
    await bot.change_presence(activity=discord.Game(name=random.choice(activities)))

#Welcomes new member in channel decided in config and assigns welcome role also in config
@bot.event
async def on_member_join(member):
    print("Recognised that a member called " + member.name + " joined")
    try: 
        await CHANNEL.send("Welcome " + member.mention + " to the server!!!")
        print("Sent message to " + member.name)
    except:
        print("Couldn't message " + member.name)
    await member.add_roles(ROLE)

                                
#Chat Watch


@bot.event
async def on_message(message):
    #stops jeeves responding to itself
    if message.author == bot.user:
        return
    #funny test function - quote b99
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    if message.content == '99':
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)

    #Tenor Gif Censorship, allows link embeds but removes all gifs from channel decided in config
    if "tenor.com/view" in message.content and CENSOR:
        if message.channel.id == GIF:
            await message.delete()
            await message.channel.send("No Gifs in %s %s " % (bot.get_channel(GIF).mention, message.author.mention))
            print ("Gif detected in %s posted by %s" % (bot.get_channel(GIF),message.author))

    #Pays Respects    
    if message.content == 'f':
        await message.channel.send(message.author.mention + ' sends their respects')
        print (message.channel.id)

    await bot.process_commands(message)

   
bot.run(TOKEN)
