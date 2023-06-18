from discord.ext import commands

class Intermediate(commands.Cog):

    valid_roles = ["Intermediate","Advance","Owner"]

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["delete"])
    @commands.has_any_role(*valid_roles)
    async def delete_message(self, ctx, message_id: int):
        channel = ctx.channel
        message = await channel.fetch_message(message_id)
        await ctx.message.delete()
        await message.delete()

    @commands.command(aliases=["terminate"])
    @commands.has_any_role(*valid_roles)
    async def shutdown(self, ctx):
        await ctx.send(f"{ctx.author.mention} -_Turning Off_- ~~~")
        await self.bot.close()

async def setup(bot):
    await bot.add_cog(Intermediate(bot))