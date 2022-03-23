import subprocess

import config

copypasta1 = """*jaw drops to floor, eyes pop out of sockets accompanied by trumpets, heart beats out of chest, 
awooga awooga sound effect, pulls chain on train whistle that has appeared next to head as steam blows out, 
slams fists on table, rattling any plates, bowls or silverware, whistles loudly, fireworks shoot from top of head, 
pants loudly as tongue hangs out of mouth, wipes comically large bead of sweat from forehead, clears throat, 
straightens tie, combs hair* Ahem, you look very lovely."""

vgmgRules = """**-Rules-**  

1. Each song has 2 points attached to it. Guessing the song title gives you 1 point, and guessing the game title gives you 1 point.

2. 0.5 points will be given for partial guesses. 

3. Search engines are not allowed. Hints will be given half way through the song.

4. Only Western localised titles accepted. No unofficial translations. 

5. Punctuation such as full stops, colons, etc... in titles do not matter.

6. You can use abbreviations or shortenings for game titles as long as they are recognizable.

7. Please try to guess the entire title, including its number in the series if it is part of one.

8. All decisions are subject to committee discretion.

9. Submit your final answers in a text document to a committee member or helper when the game is over and it will be marked!!"""

lemonade = """
```All right, I've been thinking. When life gives you lemons? Don't make lemonade. 
Make life take the lemons back! Get mad! 'I don't want your damn lemons! What am I supposed to do with these?`
Demand to see life's manager! Make life rue the day it thought it could give Gurg lemons! Do you know who I am? 
I'm the man who's going to burn your house down! With the lemons! 
I'm going to get my engineers to invent a combustible lemon that burns your house down!```"""

glados_quotes = [
    "Oh... It's you.", "It's been fun. Don't come back.",
    "This next test involves turrets. You remember them, right? They're the pale spherical things that "
    "are full of bullets. Oh wait. That's you in five seconds.",
    "Momentum; a function of mass and velocity; is conserved between portals.\nIn layman's terms: speedy "
    "thing goes in, speedy thing comes out.",
    "Did you know you can donate one or all of your vital organs to the Edinburgh Gamesoc Self-Esteem "
    "Fund for Girls? It's true!",
    "Remember, the Edinburgh Gamesoc \"Bring Your Daughter to Work Day\" is the perfect time to have her "
    "tested.",
    "How are you holding up? BECAUSE I'M A POTATO.",
    "I think we can put our differences behind us. For science. You monster.",
    "Let's get mad! If we're going to explode, let's at least explode with some dignity.",
    "Although the euthanizing process is remarkably painful, eight out of ten Edinburgh Gamesoc "
    "Moderators believe that the Companion Cube is most likely incapable of feeling much pain. "
]

lemon_quotes = [
    "Welcome, gentlemen, to Edinburgh Gamesoc. V-Tubers, Memers, Gamers--you're here because we want the best, "
    "and you are it. So: Who is ready to play some games?",
    "Now, you already met one another on the limo ride over, so let me introduce myself. I'm Gurg. I own the place.",
    "They say great gaming is built on the shoulders of giants. Not here. At Gamesoc, we do all our gaming from level "
    "1. No hand holding. "
]

# funny test function - quote b99
brooklyn_99_quotes = [
    'I\'m the human form of the 💯 emoji.',
    'Bingpot!',
    (
        'Cool. Cool cool cool cool cool cool cool, '
        'no doubt no doubt no doubt no doubt.'
    ),
]

misha = "<:misha:694298077565026396>"

glados_startup = [
    "Oh... It's you.",
    "It's been a long time. How have you been?",
    "I've been really busy being dead. You know, after you MURDERED ME.",
    "Can you hear me?",
    "Do not touch the operational end of The Device.",
    "Do not look directly at the operational end of The Device."
]

activities = [
    'World Domination',
    'The Matrix',
    'Adventure Time',
    '💯',
    'Dying Inside',
    'Poggers',
    'Ping @TTChowder'
]


def introduction(new_member_mention: str) -> str:
    # ugly indentation, feel free to fix
    return f"""
Welcome {new_member_mention} to the server!!!
Bot help command is ~help, feel free to use it in <#{config.BOTCHANNEL}> to add yourself to game roles so you can get notified 
React to the relevant messages in <#{config.ROLECHANNEL}> to give yourself access to various channels on the server"""


def fortune() -> str:
    if config.TEST:
        return "fortune"
    return subprocess.check_output('fortune | cowsay', shell=True, universal_newlines=True)


def moo() -> str:
    if config.TEST:
        return "moo"
    return subprocess.check_output("cowsay \"Have you moo\'d today?\"", shell=True, universal_newlines=True)
