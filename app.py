import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)
        self.guild_id = int(os.getenv("GUILD_ID"))

    async def setup_hook(self):
        await self.load_extension("cogs.diceCog")
        print("✅ diceCog chargé")
        await self.load_extension("cogs.genieCog")
        print("✅ genieCog chargé")
        synced = await self.tree.sync(guild=discord.Object(id=self.guild_id))
        print(f"✅ {len(synced)} commandes synchronisées")
        for commands in synced:
            print(f"- {commands}")

    async def on_ready(self):
        print(f"✅ Connecté en tant que {self.user} (ID: {self.user.id})")

async def run():
    token = os.getenv("BOT_TOKEN")
    async with MyBot() as bot:
        await bot.start(token)

if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\n🛑 Bot arrêté proprement")