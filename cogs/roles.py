from discord.ext import commands
import discord
import asyncio
import re

from modules.utility import Utility
from modules.UI import RoleButton


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
        # channel = guild.get_channel(payload.channel_id)
        # message = await channel.fetch_message(payload.message_id)

        # role_channel = next((channel for channel in user.guild.text_channels if channel.name in [
        #                        "role", "roles"]), None)
        # data_message = [message.embeds[0].to_dict() async for message in role_channel.history(limit=None)]

        for role_assigner in self.fetch_json("roles.json").get("role-assignment"):
            if str(payload.message_id) == role_assigner.get("message_id"):
                for roles in role_assigner.get("roles"):
                    for role, emoji in roles.items():
                        if self.emoji_translator(
                            user, payload.emoji.name
                        ) == self.emoji_translator(user, emoji):
                            role = discord.utils.get(guild.roles, name=f"{role}")
                            await user.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)
        # channel = guild.get_channel(payload.channel_id)
        # message = await channel.fetch_message(payload.message_id)

        # role_channel = next((channel for channel in user.guild.text_channels if channel.name in [
        #                        "role", "roles"]), None)
        # data_message = [message.embeds[0].to_dict() async for message in role_channel.history(limit=None)]

        for role_assigner in self.fetch_json("roles.json").get("role-assignment"):
            if str(payload.message_id) == role_assigner.get("message_id"):
                for roles in role_assigner.get("roles"):
                    for role, emoji in roles.items():
                        if self.emoji_translator(
                            user, payload.emoji.name
                        ) == self.emoji_translator(user, emoji):
                            role = discord.utils.get(guild.roles, name=f"{role}")
                            await user.remove_roles(role)

    @commands.command(aliases=["fg","guild","bureau"])
    async def formerguild(self, ctx, bureau_name: str = None, hex_color=None):
        role_name = f"[_ {bureau_name} _]" if bureau_name and bureau_name.strip() else None
        prev_role = next((role for role in ctx.author.roles if re.match(r"^\[.*\]$", role.name)),None)
        existing_role = next((role for role in ctx.guild.roles if role.name == role_name), None)
        color = (
            discord.Color(int(hex_color, 16))
            if hex_color is not None
            else discord.Color.from_rgb(198, 175, 165)
        )

        if bureau_name is None or not bureau_name.strip():
            if prev_role:
                await ctx.author.remove_roles(prev_role)
                if len(prev_role.members) < 1:
                    await prev_role.delete()
            return

        if prev_role:
            await ctx.author.remove_roles(prev_role)
            if len(prev_role.members) < 1:
                await prev_role.delete()

        role = existing_role or await ctx.guild.create_role(name=role_name, color=color)
        await ctx.author.add_roles(role)

    @commands.command()
    async def ign(self, ctx, name=None, id: str = None, hex_color=None):
        role_name = f">{id}<" if id and id.strip() else None
        prev_role = next((role for role in ctx.author.roles if re.match(r'^>.*<$', role.name)), None)
        existing_role = next((role for role in ctx.guild.roles if role.name == role_name), None)
        color = discord.Color(int(hex_color, 16)) if hex_color is not None else discord.Color.from_rgb(198, 175, 165)
        member = ctx.author
        embed = discord.Embed()

        if existing_role:
            if existing_role == prev_role:
                embed.title = f"id:{id} Already Taken by You!"
                embed.color = discord.Color.from_rgb(144, 238, 144)
                await ctx.send(embed=embed)
                return
            else:
                embed.title = f"id:{id} Already Taken by {existing_role.members[0]}"
                embed.color = discord.Color.from_rgb(243, 58, 106)
                await ctx.send(embed=embed)
                return

        if name is None or not name.strip():
            if prev_role:
                await ctx.author.remove_roles(prev_role)
                if len(prev_role.members) < 1:
                    await prev_role.delete()
            if member.nick:
                await member.edit(nick=None)  # Revert to the default nickname if it's not None
            return

        if prev_role:
            await ctx.author.remove_roles(prev_role)
            if len(prev_role.members) < 1:
                await prev_role.delete()

        role = await ctx.guild.create_role(name=role_name, color=color)
        await member.edit(nick=str(name))
        await member.add_roles(role)

    @commands.command(name="ra")
    async def role_assigner(self, ctx):
        if ctx.author != ctx.guild.owner:
            return

        role_names = self.fetch_json("roles.json").get("role-assignment-interaction")
        role_mentions = [discord.utils.get(ctx.guild.roles, name=role_name).mention for role_name in role_names]

        embed = discord.Embed(title="Role-Assignment", description="\n".join(role_mentions))

        view = discord.ui.View()
        for role_name in role_names:
            view.add_item(RoleButton(role_name))

        await ctx.send("Click the button to assign roles.", embed=embed, view=view, delete_after=10)
        await ctx.message.delete()


async def setup(bot):
    await bot.add_cog(Roles(bot))
