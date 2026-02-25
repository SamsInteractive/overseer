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
    print(f"{getattr(Color, color, Color.end)}[INFO]: {message}{Color.end}")

def success(message: str):
    print(f"{Color.green}[INFO]: {message}{Color.end}")


class Bot(commands.Bot):
    async def on_ready(self):
        success(f"Logged in as '{self.user}' (ID: {self.user.id})")
        if config.bot.status.enabled:
            info("Attempting to update bot status activity...")
            try:
                await bot.change_presence(activity=discord.Activity(
                    type=getattr(discord.ActivityType, config.bot.status.activity),
                    name=config.bot.status.name)
                )
                success(f"Successfully changed status to: "
                     f"'{config.bot.status.activity}: "
                     f"{config.bot.status.name}'")
            except Exception as e:
                error(f"Failed to update bot status: {e}")
        else:
            info("Status messages disabled in config. Skipping...")


config = load_config()
intents = discord.Intents.all()
intents.presences = False

if not config.bot.prefix:
    raise KeyError(f"bot.prefix: {config.bot.prefix}")

bot = Bot(command_prefix=config.bot.prefix, intents=intents)


async def load_cogs():
    info("Attempting to load cogs...")
    if 'cogs' in os.listdir():
        cogs_loaded = 0
        for cog in os.listdir('./cogs'):
            if cog.endswith('.py'):
                try:
                    await bot.load_extension(cog)
                    cogs_loaded += 1
                    success(f"Successfully loaded cog '{cog}'")
                except Exception as e:
                    warn(f"Failed to load cog '{cog}': {e}")
        success(f"Finished loading {cogs_loaded} cogs.")
    else:
        warn("Attempted to load cogs but no directory was found.")


if __name__ == "__main__":
    asyncio.run(load_cogs())
    bot.run(os.environ['bot_token'])