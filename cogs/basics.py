import discord
from discord.ext import commands
from discord import app_commands
from overseer import error, warn, info, success

class Basics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='help',
        description='Display information about bot commands.',
        extras={'usage': "/help"})
    async def help(self, interaction: discord.Interaction):
        _loaded_commands = {}
        for command in self.bot.tree.get_commands():
            try:
                if command.__class__.__name__ in _loaded_commands:
                    _loaded_commands[type(command.binding).__name__].append(
                        f"{command.extras['usage']}: "
                        f"{command.description}"
                    )
                else:
                    _loaded_commands[type(command.binding).__name__] = [
                        f"{command.extras['usage']}: "
                        f"{command.description}",]
            except Exception as e:
                warn(f"Failed to retrieve requested command info "
                     f"for {command.name}: {e}")

        loaded_commands = '\n'.join(
            f"**[{category}]**\n" + f"```{'\n'.join(commands)}```"
            for category, commands in _loaded_commands.items())

        await interaction.response.send_message(loaded_commands)


async def setup(bot):
    await bot.add_cog(Basics(bot))