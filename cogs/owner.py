from discord.ext import commands
import discord
import asyncio
from pytube import YouTube

class Owner(commands.Cog):

    valid_roles = ["Owner"]
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role(*valid_roles)
    async def leave_server(self, ctx):
        await ctx.send(f"{ctx.author.mention} I'm leaving!!!")
        await self.bot.get_guild(int(ctx.guild.id)).leave()
    
    @commands.command()
    @commands.has_any_role(*valid_roles)
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        if ctx.author.guild_permissions.kick_members:
            await user.kick(reason=reason)
            await ctx.send(f"{user.mention} has been kicked from the server. Reason: {reason}")
        else:
            await ctx.send("You do not have the required permissions to kick members.")

    @commands.command()
    @commands.has_any_role(*valid_roles)
    async def addrole(self, ctx, role_name: str, hex_color: str = "", user: discord.Member = None):
        if user is None:
            user = ctx.author

        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role:
            try:
                await user.add_roles(role)
                await ctx.send(f"Added role `{role_name}` to {user.mention}")
            except discord.Forbidden:
                await ctx.send("I don't have permission to add roles to that user!")
        else:
            try:
                if hex_color:
                    role = await ctx.guild.create_role(name=role_name, color=discord.Color(int(hex_color, 16)))
                else:
                    role = await ctx.guild.create_role(name=role_name)
            except discord.Forbidden:
                await ctx.send("I don't have permission to create roles!")
                return

            try:
                await user.add_roles(role)
                await ctx.send(f"Added role `{role_name}` to {user.mention}")
            except discord.Forbidden:
                await ctx.send("I don't have permission to add roles to that user!")
    @commands.command()
    @commands.has_any_role(*valid_roles)
    async def removerole(self, ctx, role_name: str, user: discord.Member = None):
        if user is None:
            user = ctx.author

        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if not role:
            await ctx.send(f"The role `{role_name}` doesn't exist!")
            return
        
        try:
            await user.remove_roles(role)
            await ctx.send(f"Removed role `{role_name}` from {user.mention}")
        except discord.Forbidden:
            await ctx.send("I don't have permission to remove roles from that user!")
    
    @commands.command(aliases=["prename","pname"])
    @commands.has_any_role(*valid_roles)
    async def pnickname(self, ctx, new_nickname, user=None):
        await ctx.message.delete()
        if not user:
            target_user = ctx.author
        else:
            if not ctx.message.mentions:
                await ctx.author.send("Please mention a user to change their nickname!")
                return
            target_user = ctx.message.mentions[0] 
        
        try:
            await target_user.edit(nick=new_nickname)
        except discord.Forbidden:
            pass

    # todo move this into player.py (create one)
    @commands.command()
    @commands.has_any_role(*valid_roles)
    async def play(self, ctx, link=None):
        voice_channel = ctx.author.voice.channel if ctx.author.voice else None
        if voice_channel is None and ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
            return

        if ctx.voice_client is not None:
            if ctx.voice_client.channel == voice_channel:
                return
            else:
                await ctx.voice_client.move_to(voice_channel)
        else:
            await voice_channel.connect()

        video_url = link or "https://youtu.be/d8rzpLfZXLU"
        youtube = YouTube(video_url)

        async def fetch_audio_url():
            # audio_url = youtube.streams.filter(only_audio=True).first().url
            audio_url = youtube.streams.get_highest_resolution().url
            return audio_url

        try:
            audio_url = await asyncio.wait_for(fetch_audio_url(), timeout=1)
            thumbnail_url = youtube.thumbnail_url
            embed = discord.Embed(
                title='_Now_Playing_',
                description=youtube.title,
                color=discord.Color.from_rgb(198, 175, 165),
            )
            embed.set_thumbnail(url=thumbnail_url)
            await ctx.send(embed=embed)

            audio_source = await discord.FFmpegOpusAudio.from_probe(audio_url)
            ctx.voice_client.play(audio_source, after=lambda e: print("Hello, world!"))

        except asyncio.TimeoutError:
            print("Timeout occurred while fetching audio URL")

async def setup(bot):
    await bot.add_cog(Owner(bot))