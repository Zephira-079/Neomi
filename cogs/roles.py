from discord.ext import commands
import discord

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == 1121581559695278292 and payload.user_id != self.bot.user.id:
            guild = self.bot.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)
            channel = guild.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)

    @commands.command()
    async def get(self, ctx):
        channel_name = "role"

        for guild in self.bot.guilds:
            channel = discord.utils.get(guild.text_channels, name=channel_name)
            
            if channel:
                messages = await channel.history(limit=None).flatten()

                for message in messages:
                    print(message.content)
                break  # Exit the loop if the channel is found
        if not channel:
            print(f"Channel '{channel_name}' not found.")



async def setup(bot):
    await bot.add_cog(Roles(bot))