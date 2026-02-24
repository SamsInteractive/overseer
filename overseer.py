import discord
from discord.ext import commands
import asyncio
import os

from config import load_config


class Color:
    red = '\033[91m'
    green = '\033[92m'
    yellow = '\033[93m'
    blue = '\033[94m'
    end = '\033[0m'

def warn(message: str):
    print(f"{Color.yellow}[WARN]: {Color.end}{message}")

def error(message: str):
    print(f"{Color.yellow}[ERROR]: {Color.end}{message}")

def info(message: str, color='end'):
    print(f"[INFO]: {getattr(Color, color, Color.end)}{message}{Color.end}")


class Bot(commands.Bot):
    async def on_ready(self):
        info(f"Logged in as {self.user} (ID: {self.user.id})")
        info("Attempting to update bot status activity...")
        try:
            await bot.change_presence(activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=config.bot.status.name)
            )
        except Exception as e:
            print(f"Failed to update bot status: {e}")



config = load_config()
intents = discord.Intents.all()
intents.presences = False

if not config.bot.prefix:
    raise KeyError(f"bot.prefix: {config.bot.prefix}")

bot = Bot(command_prefix=config.bot.prefix, intents=intents)


async def load_cogs():
    print("Attempting to load cogs...")
    if 'cogs' in os.listdir():
        cogs_loaded = 0
        for cog in os.listdir('./cogs'):
            if cog.endswith('.py'):
                try:
                    await bot.load_extension(cog)
                    cogs_loaded += 1
                    print(f"{Color.green}Successfully loaded cog '{cog}'{Color.end}")
                except Exception as e:
                    print(f"Failed to load cog '{cog}': {e}")
        print(f"Finished loading {cogs_loaded} cogs.")
    else:
        print("WARN: Attempted to load cogs but no directory was found.")


if __name__ == "__main__":
    asyncio.run(load_cogs())
    bot.run(os.environ['bot_token'])