import discord
import re
from discord.ext import commands
from discord import app_commands
import asyncio
from discord import File
from utils.quote_image import create_quote_image
import os

class QuoteCog(commands.Cog):
    """Cog pour gérer les citations stylisées"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    async def replace_mentions_with_names(text: str, guild: discord.Guild) -> str:
        """
        Remplace les mentions par le nom, même si l'utilisateur est hors-ligne.
        """
        matches = re.findall(r"<@!?(\d+)>", text)
        for user_id_str in matches:
            user_id = int(user_id_str)
            member = guild.get_member(user_id)
            if not member:
                try:
                    member = await guild.fetch_member(user_id)
                except discord.NotFound:
                    continue
                except discord.HTTPException:
                    continue
            
            if member:
                text = re.sub(r"<@!?" + user_id_str + r">", member.display_name, text)
        return text

    @app_commands.command(
        name="quote",
        description="Crée une citation stylisée avec fond uni et auteur(s)"
    )
    @app_commands.describe(
        message="Le texte de la citation",
        author="Auteur(s) de la citation (mentions possibles et texte libre)"
    )
    async def quote(self, interaction: discord.Interaction, message: str, author: str):
        if len(message) > 250:
            return await interaction.response.send_message("❌ Ta citation est trop longue (max 250 caractères) !", ephemeral=True)
        author = await QuoteCog.replace_mentions_with_names(author, interaction.guild)
        image_bytes = create_quote_image(message, author)
        file = File(fp=image_bytes, filename="quote.png")
        await interaction.response.send_message(file=file)

async def setup(bot: commands.Bot):
    cog = QuoteCog(bot)
    await bot.add_cog(cog)