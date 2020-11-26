import discord
import asyncio
import random
from config import TOKEN,ROLE,CHANNEL

intents = discord.Intents.all()

client = discord.Client(intents=intents)

activities = ['World Domination', 'The Matrix', 'Your Mum']

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(activity=discord.Game(name=random.choice(activities)))

@client.event
async def on_member_join(member):
    print("Recognised that a member called " + member.name + " joined")
    channel = discord.utils.get(member.guild.channels, name='general')
    ROLE = discord.utils.get(member.guild.roles, name='Member')
    try: 
        await channel.send("Welcome " + member.mention + " to the server!!!")
        print("Sent message to " + member.name)
    except:
        print("Couldn't message " + member.name)
    await member.add_roles(ROLE)

                                
    
@client.event
async def on_message(message):
    #stops jeeves responding to itself
    if message.author == client.user:
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

    if message.content == '!99':
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)

    if message.content == '!hello':
        await message.channel.send("Hello")
        
    if message.content == 'f':
        await message.channel.send(message.author.mention + ' sends their respects')
        print (message.channel.id)
    
client.run(TOKEN)
