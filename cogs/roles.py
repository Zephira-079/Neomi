from discord.ext import commands
import discord
import asyncio

from cogs.utility import Utility

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.react_message = Utility().react_message
        self.fetch_json = Utility().fetch_json
        self.emoji_translator = Utility().emoji_translator
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)
        channel = guild.get_channel(payload.channel_id)
        # message = await channel.fetch_message(payload.message_id)

        role_channel = next((channel for channel in user.guild.text_channels if channel.name in [
                               "role", "roles"]), None)
        data_message = [message.embeds[0].to_dict() async for message in role_channel.history(limit=None)]

        for role_assigner in self.fetch_json("roles.json").get("role-assignment"):
            if str(payload.message_id) == role_assigner.get("message_id"):
                for roles in role_assigner.get("roles"):
                    for role, emoji in roles.items():
                        if self.emoji_translator(user, payload.emoji.name) == self.emoji_translator(user, emoji):
                            role = discord.utils.get(guild.roles, name=f"{role}")
                            await user.add_roles(role)
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)
        channel = guild.get_channel(payload.channel_id)
        # message = await channel.fetch_message(payload.message_id)

        role_channel = next((channel for channel in user.guild.text_channels if channel.name in [
                               "role", "roles"]), None)
        data_message = [message.embeds[0].to_dict() async for message in role_channel.history(limit=None)]

        for role_assigner in self.fetch_json("roles.json").get("role-assignment"):
            if str(payload.message_id) == role_assigner.get("message_id"):
                for roles in role_assigner.get("roles"):
                    for role, emoji in roles.items():
                        if self.emoji_translator(user, payload.emoji.name) == self.emoji_translator(user, emoji):
                            role = discord.utils.get(guild.roles, name=f"{role}")
                            await user.remove_roles(role)

    @commands.command()
    async def embedpoll(self, ctx, *args):
        await ctx.message.delete()

        title = args[0] if args else "None"
        arguments = args[1:]
        descriptions = "\n".join([description for item, description in enumerate(arguments) if not item % 2])
        reactions = [description for item, description in enumerate(arguments) if item % 2]

        embed = discord.Embed(title=title, description=f"{descriptions}", color=self.bot.user.color)
        message = await ctx.send(embed=embed)
        
        await asyncio.gather(*[self.react_message(ctx, react, message) for react in reactions])

async def setup(bot):
    await bot.add_cog(Roles(bot))