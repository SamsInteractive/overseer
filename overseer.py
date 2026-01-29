import discord
from discord.ext import commands
import asyncio
import os

from config import load_config


class Bot(commands.Bot):
    pass


if __name__ == "__main__":
    config = load_config()

    intents = discord.Intents.all()
    intents.presences = False

    if not config.get("bot.prefix"):
        raise KeyError("bot.prefix")

    bot = Bot(command_prefix=config.bot.prefix, intents=intents)