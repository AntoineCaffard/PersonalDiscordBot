import discord
from discord.ext import commands
from discord import app_commands

class moodCalendarCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="mood", description="permet d'entrer votre humeur du jour")
    async def defineMood(self, interaction: discord.Interaction, color: str, date: str=None):
        return
    
    @app_commands.command(name="mood_display", description="permet de voir votre calendrier d'humeur pour un mois precis")
    async def moodDisplay(self, interaction: discord.Interaction, month: str=None):
        return
    
    @app_commands.command(name="mood_stats", description="permet de voir votre calendrier d'humeur pour un mois precis")
    async def moodStats(self, interaction: discord.Interaction):
        return