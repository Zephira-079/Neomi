from discord.ext import commands
import discord
from modules.utility import Utility
from datetime import timedelta

# todo ctx.guild.owner == ctx.author
class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fetch_json = Utility().fetch_json
        self.edit_member_roles = Utility().edit_member_roles

    @commands.command(aliases=["quit_server"])
    async def leave_server(self, ctx):
        if ctx.author != ctx.guild.owner:
            return
        await ctx.send(f"{ctx.author.mention} I'm leaving!!!")
        await self.bot.get_guild(int(ctx.guild.id)).leave()
    
    @commands.command()
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        if ctx.author != ctx.guild.owner:
            return
        if ctx.author.guild_permissions.kick_members:
            await user.kick(reason=reason)
            await ctx.send(f"{user.mention} has been kicked from the server. Reason: {reason}")
        else:
            await ctx.send("You do not have the required permissions to kick members.")

    @commands.command()
    async def addrole(self, ctx, role_name: str, hex_color: str = "", user: discord.Member = None):
        if ctx.author != ctx.guild.owner:
            return
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
    async def removerole(self, ctx, role_name: str, user: discord.Member = None):
        if ctx.author != ctx.guild.owner:
            return
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
    async def pnickname(self, ctx, new_nickname, user=None):
        if ctx.author != ctx.guild.owner:
            return
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
    
    @commands.command(aliases=["pc"])
    async def purgechannel(self, ctx, channel_id=None):
        if ctx.author != ctx.guild.owner:
            return
        if channel_id is None:
            channel_id = ctx.channel.id

        channel = self.bot.get_channel(int(channel_id))
        if channel is None:
            await ctx.send("Invalid channel ID.", delete_after = 10)
            return

        try:
            await channel.purge(limit=None)
            await ctx.send(f"All messages deleted in {channel.mention}.", delete_after = 10)
        except discord.Forbidden:
            await ctx.send("I don't have permission to delete messages in that channel.", delete_after = 10)
    
    @commands.command(aliases=["delete"])
    async def delete_message(self, ctx, message_id: int):
        if ctx.author != ctx.guild.owner:
            return
        
        channel = ctx.channel
        message = await channel.fetch_message(message_id)
        await ctx.message.delete()
        await message.delete()

    @commands.command(aliases=["terminate","shut"])
    async def shutdown(self, ctx):
        if ctx.author != ctx.guild.owner:
            return
        
        await ctx.send(f"{ctx.author.mention} -_Turning Off_- ~~~")
        await self.bot.close()

    @commands.command(aliases=["mm"])
    async def move_member(self, ctx, member: discord.Member, channel: discord.VoiceChannel = None):
        if ctx.author != ctx.guild.owner:
            return
        if not channel and ctx.author.voice:
            channel = ctx.author.voice.channel
        await member.move_to(channel)

    
    @commands.command(aliases=["jail"])
    async def isolate(self, ctx, member: discord.Member, hours: float = 12):
        if ctx.author != ctx.guild.owner:
            return

        await self.edit_member_roles(member, "Isolated") #"Isolated" # todo put somewhere in config files in future
        await member.timeout(timedelta(hours=hours), reason = "Isolated By Owner")

    @commands.command(aliases=["liberate","free"])
    async def release(self, ctx, member: discord.Member):
        if ctx.author != ctx.guild.owner:
            return
        
        await self.edit_member_roles(member)
        await member.timeout(None, reason = "Release By Owner")

    @commands.command(aliases=["grant"])
    async def permission(self, ctx, channel_name, tag):
        if ctx.author != ctx.guild.owner:
            return

        guild = ctx.guild
        channel = discord.utils.get(guild.channels, name=channel_name)

        if not channel:
            await ctx.send(f"Channel '{channel_name}' not found.")
            return
        
        permissions = self.fetch_json("permission.json").get(tag)
        if not permissions:
            await ctx.send(f"Invalid tag '{tag}'.")
            return
        
        #todo fix experimental
        for perm, value in permissions.items():
            try:
                await channel.set_permissions(guild.default_role, **{perm: value})
            except:
                print(f"error with : {perm} = {value}")

        await ctx.send(f"Channel permissions for '{channel_name}' have been updated using tag '{tag}'.")

    @commands.command()
    async def version(self, ctx):
        if ctx.author != ctx.guild.owner:
            return
        
        await ctx.send("<version undentified>")

    @commands.command(aliases=["create_link","ci","cl"])
    async def create_invite(self, ctx):
        if ctx.author != ctx.guild.owner:
            return
        
        welcome_channel = next((channel for channel in ctx.guild.text_channels if channel.name in [
                               "greetings", "welcome"]), None)
        invite_expiration = 60 * 60 * 24 * 30
        invite_quota = 25
        invite_url = await welcome_channel.create_invite(max_age=invite_expiration, max_uses=invite_quota)
        await ctx.message.delete()
        await ctx.send(f'Invite_Link: ||{invite_url}||', delete_after=10)
        

async def setup(bot):
    await bot.add_cog(Owner(bot))