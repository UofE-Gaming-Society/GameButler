import sys
import asyncio
from discord import Intents
from discord.ext import commands

import config


async def main():
    """Main entry point for the bot."""
    # Initialize the bot with intents and no command prefix (slash commands only)
    bot = commands.Bot(command_prefix=None, intents=Intents.all(), case_insensitive=True)

    # Add custom attributes for restart and update logic
    bot.git_update = False
    bot.restart = False

    # List of cogs to load
    cogs = [
        "GameButler",
        "GameRoleManager",
        "SpamFilter",
        "MiscCommands",
        "ErrorHandler"
    ]

    # Load all cogs asynchronously
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            print(f"Successfully loaded cog: {cog}")
        except Exception as e:
            print(f"Failed to load cog {cog}: {e}")

    # Run the bot
    try:
        await bot.start(config.TOKEN)
    except KeyboardInterrupt:
        print("Bot shutting down...")

    # Determine exit code based on restart and update flags
    # return code 0: neither restart nor update
    # return code 2: restart without update
    # return code 4: update without restart
    # return code 6: update and restart
    sys.exit(bot.restart * 2 + bot.git_update * 4)


if __name__ == "__main__":
    asyncio.run(main())
