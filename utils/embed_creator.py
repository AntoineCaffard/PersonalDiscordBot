import discord

def colorize(n, max_val, mod=0):
    if n == 1:
        return f"🔴 {n}"
    elif n == max_val + mod:
        return f"🟢 {n}"
    else:
        return f"⚪ {n}"

def dice_result_embed(user, num_dice, num_faces, modifier, results_raw, results, color=discord.Color.blue()):
    
    mod_str = f"+{modifier}" if modifier > 0 else (f"{modifier}" if modifier < 0 else "0")
    raw_str = ", ".join(str(n) for n in results_raw)
    table_str = "\n".join(colorize(n, num_faces, modifier) for n in results)
    table_str = f"```\n{table_str}\n```"

    embed = discord.Embed(title=f"{user.display_name} a lancé {num_dice}d{num_faces}", color=color)
    embed.add_field(name="Modificateur", value=mod_str, inline=False)
    embed.add_field(name="Valeurs", value=f"```\n{results_raw}\n```", inline=False)
    embed.add_field(name="Résultat", value=table_str, inline=False)
    return embed