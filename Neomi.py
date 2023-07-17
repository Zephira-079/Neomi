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
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(config.get("neomi_key"))

asyncio.run(main())
