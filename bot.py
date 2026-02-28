import os
import re
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

def parse_dice(dice_str: str):
   
    match = re.fullmatch(r"(\d+)d(\d+)([+-]\d+)?", dice_str.strip())
    if not match:
        raise ValueError(f"Format invalide : {dice_str}")
    
    num_dice = int(match.group(1))
    num_faces = int(match.group(2))
    modifier = int(match.group(3)) if match.group(3) else 0
    
    if num_dice <= 0 or num_faces <= 0:
        raise ValueError("Nombre de dés et faces doit être >= 1")
    
    return num_dice, num_faces, modifier

def colorize(n, max_val):
            if n == 1:
                return f"🔴 {n}"
            elif n == max_val:
                return f"🟢 {n}"
            else:
                return f"⚪ {n}"

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
guild_id = int(os.getenv("GUILD_ID"))

@bot.tree.command(guild=discord.Object(id=guild_id))
async def test(interaction: discord.Interaction, a: int):
     await interaction.response.send_message(f'Coucou a mes {a} copains !')

@bot.tree.command(guild=discord.Object(id=guild_id))
async def d(interaction: discord.Interaction, value: str):

    try:
        num_dice, max_val, modifier = parse_dice(value)
        results = [min(max(random.randint(1, max_val) + modifier, 1), max_val) for _ in range(num_dice)]
        mod_str = f"+{modifier}" if modifier > 0 else (f"{modifier}" if modifier < 0 else "0")
        table_str = "\n".join(colorize(n, max_val) for n in results)
        table_str = f"```\n{table_str}\n```"

        embed = discord.Embed(
            title=f"🎲 Lancer de {num_dice}d{max_val}",
            color=discord.Color.blurple()
        )
        embed.add_field(name="Modificateur", value=mod_str, inline=False)
        embed.add_field(name="Résultats", value=table_str, inline=False)

        await interaction.response.send_message(embed=embed)

    except Exception as e:
        await interaction.response.send_message(f"Erreur: {e}")

@bot.tree.command(guild=discord.Object(id=guild_id))
async def d_avantage(interaction: discord.Interaction, value: str):

    try:
        num_dice, max_val, modifier = parse_dice(value)
        results = [min(max(random.randint(1, max_val) + modifier, 1), max_val) for _ in range(num_dice)]
        mod_str = f"+{modifier}" if modifier > 0 else (f"{modifier}" if modifier < 0 else "0")
        table_str = "".join(colorize(max(results), max_val))
        table_str = f"```\n{table_str}\n```"

        embed = discord.Embed(
            title=f"🎲 Lancer avec avantage de {num_dice}d{max_val}",
            color=discord.Color.blurple()
        )
        embed.add_field(name="Modificateur", value=mod_str, inline=False)
        embed.add_field(name="Résultat", value=table_str, inline=False)

        await interaction.response.send_message(embed=embed)

    except Exception as e:
        await interaction.response.send_message(f"Erreur: {e}")

@bot.tree.command(guild=discord.Object(id=guild_id))
async def d_mj(interaction: discord.Interaction, value: str):
    try:
        num_dice, max_val, modifier = parse_dice(value)
        results = [min(max(random.randint(1, max_val) + modifier, 1), max_val) for _ in range(num_dice)]
        mod_str = f"+{modifier}" if modifier > 0 else (f"{modifier}" if modifier < 0 else "0")

        table_str = "\n".join(colorize(n, max_val) for n in results)

        embed = discord.Embed(
            title=f"🎲 Lancer de {num_dice}d{max_val}",
            color=discord.Color.blurple()
        )
        embed.add_field(name="Modificateur", value=mod_str, inline=False)
        embed.add_field(name="Résultats", value=table_str, inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    except Exception as e:
        await interaction.response.send_message(f"Erreur: {e}", ephemeral=True)

@bot.tree.command(guild=discord.Object(id=guild_id))
async def d_desavantage(interaction: discord.Interaction, value: str):

    try:
        num_dice, max_val, modifier = parse_dice(value)
        results = [min(max(random.randint(1, max_val) + modifier, 1), max_val) for _ in range(num_dice)]
        mod_str = f"+{modifier}" if modifier > 0 else (f"{modifier}" if modifier < 0 else "0")
        table_str = "".join(colorize(min(results), max_val))
        table_str = f"```\n{table_str}\n```"

        embed = discord.Embed(
            title=f"🎲 Lancer avec desavantage de {num_dice}d{max_val}",
            color=discord.Color.blurple()
        )
        embed.add_field(name="Modificateur", value=mod_str, inline=False)
        embed.add_field(name="Résultat", value=table_str, inline=False)

        await interaction.response.send_message(embed=embed)

    except Exception as e:
        await interaction.response.send_message(f"Erreur: {e}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "Bonjour" in message.content:
        await message.channel.send("Coucou les coquinous !")
    await bot.process_commands(message)

@bot.event
async def on_ready():
        print(f'Logged on as {bot.user}!')
        try: 
            synced_commands = await bot.tree.sync(guild=discord.Object(id=guild_id))
            print(f'{len(synced_commands)} commands loaded!')
        except Exception as e:
             print(e)

def launch(token) -> None:
    bot.run(token)

if __name__ == "__main__":

    launch(os.getenv("BOT_TOKEN"))