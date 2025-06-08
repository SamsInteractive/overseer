import asyncio
import os
import discord
from discord.ext import commands

class Bot(commands.Bot):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        try:
            version_tag = os.environ['version_tag']
        except:
            version_tag = 'null version'
            print('No version tag found')
        print('------\nSyncing Commands...')
        await self.tree.sync()
        print('Updating status...')
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"over the universe✨ {version_tag}"))
        print('------\nOperational!')


# Set intents | Create instance of Bot class using '!' prefix
intents = discord.Intents.all()
intents.presences = False
bot = Bot(command_prefix='!', intents=intents)


#@bot.tree.command(name='new_event', description='Track a new event')
#@app_commands.describe(event_name='Name of event', date="DD/MM/YYYY", time="hh:mm:am/pm", timezone="AEST, AEDT, NZ")
#async def new_event(interaction: discord.Interaction, event_name: str, date: str):
#    await interaction.response.send_message("Incomplete")

@bot.tree.context_menu(name="Mock")
async def mock(interaction: discord.Interaction, message: discord.Message):
    cap, result = True, ''
    try:
        for char in message.content:
            if char.isalpha():
                result += char.upper() if cap else char.lower()
                cap = not cap
            else:
                result += char
        await message.reply(result, mention_author=True)
        await interaction.response.send_message(f"Mocked {message.author}", ephemeral=True)
    except:
        await interaction.response.send_message("Error, could not complete command", ephemeral=True)



# Import cogs and run
async def load():
    extensions = list(map(lambda cog: f'cogs.{cog[:-3]}', filter(lambda cog: cog.endswith('.py') and not cog.startswith('_'), os.listdir('./cogs'))))
    for extension in extensions:
        await bot.load_extension(extension)

    if 'music_cog.py' in os.listdir('./cogs'):
        await bot.load_extension('cogs.music_cog.music')

if __name__ == '__main__':
    asyncio.run(load())
    bot.run(os.environ['overseer_token'])