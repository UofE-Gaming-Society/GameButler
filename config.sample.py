import re
from typing import List

# bot token
TOKEN = "OTU4MDcwOTI3MTYwMTE1Mjkx.YkH_FQ.I6IZBCuYnO_ciSMlVwH19D4zsyc"

# server IDs for registering slash commands
GUILD_IDS = [827253376227999804]

# Role it can assign on member joining - int
NEWMEMBERROLE = 0

# Role to assign upon accepting rules
MEMBERROLE = 0

# Role to control bot
BOT_ADMIN_ROLE = 0

# Welcome message channel - int
CHANNEL = 0

# Bot command channel id - int
BOTCHANNEL = 0

# Role selection channel id - int
ROLECHANNEL = 0

# Channel where user can accept rules - int
RULES = 0

# Game Role Colour Hexcode Lowercase - str
COLOUR = ""
HEXCOLOUR = 0x000000

# Toggle Tenor Gif censorship
CENSOR = False

# Anti-Gif Channels - which channels to enable the anti-gif-spam in
ANTI_GIF_CHANNELS: List[int] = [0]

# Anti-Gif search terms, uses regular expressions
ANTI_GIF_PATTERNS: List[re.Pattern] = [
    re.compile(r"tenor\.com/view"),
    re.compile(r"giphy\.com/media"),
    re.compile(r".*\.gif")
]

# Gif Spam Toggle - Bool
ANTISPAM = False

# GIF spam limit - int
LIMIT = 6

# Discord invite link filtering - bool
ANTI_ADVERT = False

# toggleable test mode
TEST = False

TICKET_CHANNEL = 0