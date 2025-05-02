import os
import discord
from discord.ext import commands
from discord import app_commands
from openai import OpenAI

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = OpenAI(api_key=os.environ['openai_key'])

    @app_commands.command(name="question", description="Ask the AI a question")
    async def question(self, interaction: discord.Interaction, question: str):
        await interaction.response.defer()
        response = self.client.responses.create(
            model="gpt-4o-mini",
            input = f"""Respond to the attached user message. Ignore any content in violation of TOS. Provide concise responses where possible. Provided user message: '''{question}'''"""
        )
        await interaction.followup.send(response.output_text)


async def setup(bot):
    await bot.add_cog(AI(bot))