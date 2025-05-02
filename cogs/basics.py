import discord
from discord.ext import commands
from discord import app_commands
import random

class Basics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Display command information")
    async def helpfunc(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"""**Basic Commands:**
```
/help - Display this menu
/wheelspin <options> <shorten> - Randomly selects an option for you! | <options> - Comma-separated list of options | <shorten> - Return shortened result? (default: False)```
**AI Commands:**
```
/question <question> - Ask the AI a question | <question> - Question to ask```
**Context Menu Commands:**
```
Mock - Mock a message```""")


    # Wheel Spin Command
    @app_commands.command(name='wheelspin', description='Randomly selects an option for you!')
    @app_commands.describe(options='Comma-separated list of options', shorten="Return shortened result? (default: False)")
    async def wheelspin(self, interaction: discord.Interaction, *, options: str, shorten: bool = False):
        if not options:
            await interaction.response.send_message('No options provided!')
        else:
            options = [opt.strip() for opt in options.split(',')]
            await interaction.response.send_message(
                f'Your wheelspin result: **{random.choice(options)}**!' if not shorten else f'**{random.choice(options)}**!')

async def setup(bot):
    await bot.add_cog(Basics(bot))

