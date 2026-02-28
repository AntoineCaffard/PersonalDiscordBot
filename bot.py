import os
import re
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
guild_id = int(os.getenv("GUILD_ID"))

def parse_dice(dice_str: str):
   
    match = re.fullmatch(r"(\d+)d(\d+)([+-]\d+)?", dice_str.strip())
    if not match:
        raise ValueError(f"Format invalide : {dice_str}")
    
    num_dice = int(match.group(1))
    num_faces = int(match.group(2))
    modifier = int(match.group(3)) if match.group(3) else 0
    
    if num_dice <= 0 or num_faces <= 0 or num_dice > 200:
        raise ValueError("Nombre de dés et faces doit être >= 1")
    
    return num_dice, num_faces, modifier

def colorize(n, max_val, mod=0):
            if n == 1:
                return f"🔴 {n}"
            elif n == max_val + mod:
                return f"🟢 {n}"
            else:
                return f"⚪ {n}"

def roll_dice(value, message):
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

        return embed

    except Exception as e:
        return "Error"

@bot.tree.command(guild=discord.Object(id=guild_id))
async def d(interaction: discord.Interaction, value: str):

    try:
        num_dice, max_val, modifier = parse_dice(value)
        results_raw = [random.randint(1, max_val) for _ in range(num_dice)]
        results = [min(max(value + modifier, 1), max_val) for value in results_raw]
        mod_str = f"+{modifier}" if modifier > 0 else (f"{modifier}" if modifier < 0 else "0")
        table_str = "\n".join(colorize(n, max_val) for n in results)
        table_str = f"```\n{table_str}\n```"

        embed = discord.Embed(
            title=f"🎲 Lancer de {num_dice}d{max_val}",
            color=discord.Color.blurple()
        )
        embed.add_field(name="Modificateur", value=mod_str, inline=False)
        embed.add_field(name="Valeurs", value=f"```\n{results_raw}\n```", inline=False)
        embed.add_field(name="Résultats", value=table_str, inline=False)

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
        table_str = f"```\n{table_str}\n```"

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
async def d_sum(interaction: discord.Interaction, value: str):

    try:
        num_dice, max_val, modifier = parse_dice(value)
        results = [min(max(random.randint(1, max_val), 1), max_val) for _ in range(num_dice)]
        total = sum(results) + modifier
        mod_str = f"+{modifier}" if modifier > 0 else (f"{modifier}" if modifier < 0 else "0")

        embed = discord.Embed(
            title=f"🎲 Lancer de {num_dice}d{max_val}",
            color=discord.Color.blurple()
        )
        embed.add_field(name="Modificateur", value=mod_str, inline=False)
        embed.add_field(name="Valeurs", value=f"```\n{results}\n```", inline=False)
        embed.add_field(name="Total", value=str(total), inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=False)

    except Exception as e:
        await interaction.response.send_message(f"Erreur: {e}", ephemeral=False)

@bot.tree.command(guild=discord.Object(id=guild_id))
async def d_sum_mj(interaction: discord.Interaction, value: str):

    try:
        num_dice, max_val, modifier = parse_dice(value)
        results = [min(max(random.randint(1, max_val), 1), max_val) for _ in range(num_dice)]
        total = sum(results) + modifier
        mod_str = f"+{modifier}" if modifier > 0 else (f"{modifier}" if modifier < 0 else "0")
        
        embed = discord.Embed(
            title=f"🎲 Lancer de {num_dice}d{max_val}",
            color=discord.Color.blurple()
        )
        embed.add_field(name="Modificateur", value=mod_str, inline=False)
        embed.add_field(name="Valeurs", value=f"```\n{results}\n```", inline=False)
        embed.add_field(name="Total", value=str(total), inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True) 

    except Exception as e:
        await interaction.response.send_message(f"Erreur: {e}", ephemeral=True)

@bot.tree.command(guild=discord.Object(id=guild_id))
async def d_avantage(interaction: discord.Interaction, value: str):

    try:
        num_dice, max_val, modifier = parse_dice(value)
        results_raw = [random.randint(1, max_val) for _ in range(num_dice)]
        results = [min(max(value + modifier, 1), max_val) for value in results_raw]
        mod_str = f"+{modifier}" if modifier > 0 else (f"{modifier}" if modifier < 0 else "0")
        table_str = "".join(colorize(max(results), max_val))
        table_str = f"```\n{table_str}\n```"

        embed = discord.Embed(
            title=f"🎲 Lancer avec avantage de {num_dice}d{max_val}",
            color=discord.Color.blurple()
        )
        embed.add_field(name="Modificateur", value=mod_str, inline=False)
        embed.add_field(name="Valeurs", value=f"```\n{results_raw}\n```", inline=False)
        embed.add_field(name="Résultat", value=f"```{(colorize(max(results), max_val))}```", inline=False)

        await interaction.response.send_message(embed=embed)

    except Exception as e:
        await interaction.response.send_message(f"Erreur: {e}")


@bot.tree.command(guild=discord.Object(id=guild_id))
async def d_desavantage(interaction: discord.Interaction, value: str):

    try:
        num_dice, max_val, modifier = parse_dice(value)
        results_raw = [random.randint(1, max_val) for _ in range(num_dice)]
        results = [min(max(value + modifier, 1), max_val) for value in results_raw]
        mod_str = f"+{modifier}" if modifier > 0 else (f"{modifier}" if modifier < 0 else "0")
        table_str = "".join(colorize(min(results), max_val))
        table_str = f"```\n{table_str}\n```"

        embed = discord.Embed(
            title=f"🎲 Lancer avec desavantage de {num_dice}d{max_val}",
            color=discord.Color.blurple()
        )
        embed.add_field(name="Modificateur", value=mod_str, inline=False)
        embed.add_field(name="Valeurs", value=f"```\n{results_raw}\n```", inline=False)
        embed.add_field(name="Résultat", value=f"```{(colorize(min(results), max_val))}```", inline=False)

        await interaction.response.send_message(embed=embed)

    except Exception as e:
        await interaction.response.send_message(f"Erreur: {e}")

@bot.tree.command(guild=discord.Object(id=guild_id))
async def d_moy(interaction: discord.Interaction, value: str):

    try:
        num_dice, max_val, modifier = parse_dice(value)
        results = [min(max(random.randint(1, max_val), 1), max_val) for _ in range(num_dice)]
        total = sum(results) + modifier
        mod_str = f"+{modifier}" if modifier > 0 else (f"{modifier}" if modifier < 0 else "0")

        embed = discord.Embed(
            title=f"🎲 Lancer de {num_dice}d{max_val}",
            color=discord.Color.blurple()
        )
        embed.add_field(name="Modificateur", value=mod_str, inline=False)
        embed.add_field(name="Valeurs", value=f"```\n{results}\n```", inline=False)
        embed.add_field(name="Total", value=str(total / num_dice), inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=False)

    except Exception as e:
        await interaction.response.send_message(f"Erreur: {e}", ephemeral=False)

@bot.tree.command(guild=discord.Object(id=guild_id))
async def beer(interaction: discord.Interaction):
    await interaction.response.send_message(f"Voici pour toi {interaction.user.global_name} !!! 🍺")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "chagasse" in message.content.lower():
        await message.channel.send("Ouais Emma c'est une Chagasse !!!")
    match = re.search(r"(\d+)d(\d+)([+-]\d+)?", message.content.lower())
    if (match):
        embed = roll_dice(match.group(0), message)
        await message.channel.send(embed=embed)
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