from discord.ext import commands
import discord

class Rules(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    
async def setup(bot):
    await bot.add_cog(Rules(bot))