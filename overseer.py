import discord
from discord.ext import commands
import asyncio
import os

from config import load_config


class TermColors:
    red = '\033[91m'
    green = '\033[92m'
    yellow = '\033[93m'
    blue = '\033[94m'
    end = '\033[0m'


class Bot(commands.Bot):
    async def on_ready(self):
        print(f"Logged in as {self.user} using ID: {self.user.id}")
        print("Attempting to update bot status activity...")
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
    for cog in os.listdir('./cogs'):
        if cog.endswith('.py'):
            try:
                await bot.load_extension(cog)
                print(f"Sucessfully loaded '{cog}'")
            except Exception as e:
                print(f"Failed to load cog '{cog}': {e}")


if __name__ == "__main__":
    print("Loading cogs...")
    if 'cogs' in os.listdir():
        asyncio.run(load_cogs())
    else:
        print("Attempted to load cogs but no directory was found.")
    bot.run(os.environ['bot_token'])