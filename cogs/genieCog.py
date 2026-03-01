import discord
import re
from discord.ext import commands
from discord import app_commands
from utils.genie_logic import GenieLogic
from utils.embed_creator import genie_result_embed

class GenieCog(commands.Cog):
    """Cog pour gérer la Divination"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="genie", description="consulte les astres")
    async def divination(self, interaction: discord.Interaction, question: str):
        answer = GenieLogic.get_random_answer()
        embed = genie_result_embed(interaction.user, question, answer)
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):

    cog = GenieCog(bot)
    await bot.add_cog(cog)
        