from discord.ext import commands
import discord

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # todo fix permissions
        channel = discord.utils.get(member.guild.text_channels, name=lambda n: n.lower() in ["greetings", "welcome"])

        if channel and self.bot.has_permissions(channel, send_messages=True):
            await channel.send(f"Greetings And Warm Embrace To Our Guild {member.mention}! ~ 💕")
        else:
            print("Unable to send message. Bot lacks necessary permissions.")

async def setup(bot):
    await bot.add_cog(Welcome(bot))