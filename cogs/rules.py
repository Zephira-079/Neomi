from discord.ext import commands
import discord
import json

class Rules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.resource = "./assets/json/resource_cogs"

    # todo remvoe the duplicate or move them to better script
    def fetch_json(self, path):
        with open(f"{self.resource}/{path}", 'r') as file:
            return json.load(file)

    @commands.command()
    async def rules(self, ctx):
        await ctx.message.delete()

        embed = discord.Embed(title=f"Rules", description="**Rules may subject to change**", color=discord.Color.from_rgb(198, 175, 165))

        for item in self.fetch_json("rules.json").get("rules"):
            title = item.get("title")
            description = item.get("description")
            
            embed.add_field(name=title, value=description)

        await ctx.send(embed=embed)
    
async def setup(bot):
    await bot.add_cog(Rules(bot))