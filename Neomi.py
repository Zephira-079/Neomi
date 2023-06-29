import discord
from discord.ext import commands
import asyncio

import config
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="./", intents=intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    print(f"It's your Loving Bot, {bot.user.name}! ~ 💕❤")

async def load_extensions():
    await bot.load_extension("cogs.general")
    await bot.load_extension("cogs.owner")
    await bot.load_extension("cogs.music")
    await bot.load_extension("cogs.roles")
    await bot.load_extension("cogs.welcome")
    await bot.load_extension("cogs.rules")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(config.neomi_key() or os.environ["neomi_key"])

asyncio.run(main())
