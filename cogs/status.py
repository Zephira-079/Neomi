import discord
from discord.ext import commands, tasks

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 1125383093981810698 
        self.online_message_id = 1125651638238064740
        self.update_channel_name.start()

    def cog_unload(self):
        self.update_channel_name.cancel()

    @tasks.loop(seconds=10) 
    async def update_channel_name(self):
        channel = self.bot.get_channel(self.channel_id)
        
        if channel:
            guild = channel.guild
            message = await channel.fetch_message(self.online_message_id)
            online_members = self.get_online_member_count(guild)
            embed = message.embeds[0]
            embed.description = f"```txt\n Count: {online_members}```"
            channel_name = f'Online members: {online_members}'
            await message.edit(embed=embed)
            await channel.edit(name=channel_name)

    def get_online_member_count(self, guild):
        return sum(1 for member in guild.members if member.status == discord.Status.online)

    @commands.command()
    async def check_online(self, ctx):
        online_members = self.get_online_member_count(ctx.guild)
        await ctx.send(f'Online members: {online_members}')
        
        


async def setup(bot):
    await bot.add_cog(Status(bot))