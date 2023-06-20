import discord
from discord.ext import commands
import asyncio

import config

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="./", intents=intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    print(f"It's your Loving Bot, {bot.user.name}! ~ 💕❤")

async def load_extensions():
    await bot.load_extension("cogs.basic")
    await bot.load_extension("cogs.intermediate")
    await bot.load_extension("cogs.owner")
    await bot.load_extension("cogs.music")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(config.neomi_key())

asyncio.run(main())
