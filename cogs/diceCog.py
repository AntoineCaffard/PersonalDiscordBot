import discord
import re
from discord.ext import commands
from discord import app_commands
from utils.dice_logic import DiceRoller
from utils.embed_creator import dice_result_embed
import os

class DiceCog(commands.Cog):
    """Cog pour gérer les lancers de dés"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def roll_dice(self, dice_str: str):
        num_dice, num_faces, modifier = DiceRoller.parse(dice_str)
        results_raw = DiceRoller.roll(num_dice, num_faces)
        final_results = DiceRoller.applyModifier(results_raw, modifier)
        return num_dice, num_faces, modifier, results_raw, final_results
    
    async def _send_dice(self, interaction: discord.Interaction, dice: str, mode="normal", hidden=False):
        try:
            num_dice, num_faces, modifier, results_raw, final_results = self.roll_dice(dice)

            if mode == "avantage":
                final_results = [max(final_results)]
            elif mode == "desavantage":
                final_results = [min(final_results)]
            elif mode == "total":
                final_results = [DiceRoller.apply_sum_modifier(results_raw, modifier)]
            elif mode == "moyenne":
                final_results = [sum(results_raw) / num_dice]
            embed = dice_result_embed(interaction.user, num_dice, num_faces, modifier, results_raw, final_results)
            await interaction.response.send_message(embed=embed, ephemeral=hidden)

        except ValueError as e:
            await interaction.response.send_message(f"❌ Erreur : {e}", ephemeral=True)

    @app_commands.command(name="d", description="Lance un ou plusieurs dés")
    @app_commands.describe(dice="Exemple : 1d20, 2d6, 4d10+3")
    async def diceRoll(self, interaction: discord.Interaction, dice: str):
       await self._send_dice(interaction, dice, mode="normal")

    @app_commands.command(name="d_mj", description="Lance un ou plusieurs dés")
    @app_commands.describe(dice="Exemple : 1d20, 2d6, 4d10+3")
    async def diceRollMJ(self, interaction: discord.Interaction, dice: str):
       await self._send_dice(interaction, dice, mode="normal", hidden=True)

    @app_commands.command(name="d_adv", description="Lance un ou plusieurs dés et renvoie le maximum")
    @app_commands.describe(dice="Exemple : 1d20, 2d6, 4d10+3")
    async def diceRollAdv(self, interaction: discord.Interaction, dice: str):
        await self._send_dice(interaction, dice, mode="avantage")

    @app_commands.command(name="d_adv_mj", description="Lance un ou plusieurs dés et renvoie le maximum")
    @app_commands.describe(dice="Exemple : 1d20, 2d6, 4d10+3")
    async def diceRollAdvMJ(self, interaction: discord.Interaction, dice: str):
        await self._send_dice(interaction, dice, mode="avantage", hidden=True)

    @app_commands.command(name="d_dis", description="Lance un ou plusieurs dés et renvoie le minimum")
    @app_commands.describe(dice="Exemple : 1d20, 2d6, 4d10+3")
    async def diceRollDis(self, interaction: discord.Interaction, dice: str):
        await self._send_dice(interaction, dice, mode="desavantage")

    @app_commands.command(name="d_dis_mj", description="Lance un ou plusieurs dés et renvoie le minimum")
    @app_commands.describe(dice="Exemple : 1d20, 2d6, 4d10+3")
    async def diceRollDisMJ(self, interaction: discord.Interaction, dice: str):
        await self._send_dice(interaction, dice, mode="desavantage", hidden=True)

    @app_commands.command(name="d_sum", description="Lance un ou plusieurs dés et renvoie la somme")
    @app_commands.describe(dice="Exemple : 1d20, 2d6, 4d10+3")
    async def diceRollSum(self, interaction: discord.Interaction, dice: str):
        await self._send_dice(interaction, dice, mode="total")
    
    @app_commands.command(name="d_sum_mj", description="Lance un ou plusieurs dés et renvoie la somme")
    @app_commands.describe(dice="Exemple : 1d20, 2d6, 4d10+3")
    async def diceRollSumMJ(self, interaction: discord.Interaction, dice: str):
        await self._send_dice(interaction, dice, mode="total", hidden=True)

    @app_commands.command(name="d_moy", description="Lance un ou plusieurs dés et renvoie la somme")
    @app_commands.describe(dice="Exemple : 1d20, 2d6, 4d10+3")
    async def diceRollMoy(self, interaction: discord.Interaction, dice: str):
        await self._send_dice(interaction, dice, mode="moyenne")


    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        matches = re.finditer(r"(\d+)d(\d+)([+-]\d+)?", message.content.lower())
        for match in matches:
            try:
                dice_str = match.group(0)
                num_dice, num_faces, modifier, results_raw, final_results = self.roll_dice(dice_str)
                embed = dice_result_embed(message.author, num_dice, num_faces, modifier, results_raw, final_results)
                await message.channel.send(embed=embed)
            except ValueError:
                continue
        await self.bot.process_commands(message)

async def setup(bot: commands.Bot):

    cog = DiceCog(bot)
    await bot.add_cog(cog)

    guild_id = int(os.getenv("GUILD_ID"))
    guild = discord.Object(id=guild_id)

    for cmd in [cog.diceRoll, cog.diceRollAdv, cog.diceRollDis, cog.diceRollSum, cog.diceRollMoy,
    cog.diceRollMJ, cog.diceRollAdvMJ, cog.diceRollDisMJ, cog.diceRollSumMJ]:
        bot.tree.add_command(cmd, guild=guild)