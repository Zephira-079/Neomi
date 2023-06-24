from discord.ext import commands
import discord

class Rules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def nothin(self, ctx):
        pass
    
async def setup(bot):
    await bot.add_cog(Rules(bot))