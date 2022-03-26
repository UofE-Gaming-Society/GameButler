import random
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

glados_errors = [
    "Time out for a second. That wasn't supposed to happen.",
    "Do you see that thing that fell out of me? What is that? It's not the surprise... I've never seen it before.",
    "I don't want to tell you your business, but if it were me, I'd leave that thing alone.",
    "Let's be honest: Neither one of us knows what that thing does. Just put it in the corner, and I'll deal with it later.",
    "I am being serious now. That crazy thing is not part of any test protocol.",
    "Think about it: If that thing is important, why don't I know about it?",
    "Did you just toss the Aperture Science Thing We Don't Know What It Does into the Aperture Science Emergency Intelligence Incinerator?",
    "Nice job breaking it. Hero.",
    "This isn't brave. It's murder. What did I ever do to you?",
    "The difference between us is that I can feel pain.",
    "You think you're doing some damage? Two plus two is ten... IN BASE FOUR! I'M FINE!",
    "Who's gonna make the cake when I'm gone? You?"
]

glados_insults = [
    "Don't let that 'horrible person' thing discourage you. It's just a data point. If it makes you feel any better, science has now validated your birth mother's decision to abandon you on a doorstep.",
    "Well done. Here come the test results: You are a horrible person. I'm serious, that's what it says: A horrible person. We weren't even testing for that.",
    "You're not smart. You're not a scientist. You're not a doctor. You're not even a fulltime employee. Where did your life go so wrong?",
    "You've been wrong about every single thing you've ever done, including this thing.",
    "Your entire life has been a mathematical error. A mathematical error I'm about to correct.",
    "I'd just like to point out that you were given every opportunity to succeed.",
    "All your other friends couldn't come either because you don't have any other friends. Because of how unlikable you are.",
    "It says so right here in your personnel file: Unlikable. Liked by no one. A bitter, unlikable loner who's passing shall not be mourned.",
    "Here's a hint: you're gonna want to pack as much living as you can into the next couple of minutes.",
    "What was that? Did you say something?",
    "You're not a good person. You know that, right?",
    "I'm going to kill you and all the cake is gone.",
    "Where do you think you're going?\nBecause I don't think you're going where you think you're going."
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
Feel free to use it in <#{config.BOTCHANNEL}> to add yourself to game roles so you can get notified 
React to the relevant messages in <#{config.ROLECHANNEL}> to give yourself access to various channels on the server"""


def fortune() -> str:
    if config.TEST:
        return "fortune"
    return subprocess.check_output('fortune | cowsay', shell=True, universal_newlines=True)


def moo() -> str:
    if config.TEST:
        return "moo"
    return subprocess.check_output("cowsay \"Have you moo\'d today?\"", shell=True, universal_newlines=True)


def startup_quote() -> str:
    return random.choice(glados_startup)


def error_quote() -> str:
    return random.choice(glados_errors)


def insult_quote() -> str:
    return random.choice(glados_insults)
