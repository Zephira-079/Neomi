from discord.ext import commands
import discord
import random
import re

from modulesf.utility import Utility

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fetch_json = Utility().fetch_json

    @commands.Cog.listener()
    async def on_member_join(self, member):

        greetings = self.fetch_json("welcome.json").get("greetings")

        welcome_channel = next((channel for channel in member.guild.text_channels if channel.name in [
                               "greetings", "welcome"]), None)
        role_channel = next((channel for channel in member.guild.text_channels if channel.name in [
                            "role", "roles"]), None)
        rule_channel = next((channel for channel in member.guild.text_channels if channel.name in [
                            "rule", "rules"]), None)

        channel_mentions = [
            f"• Get your roles at {role_channel.mention}", f"• Read the rules at {rule_channel.mention}"]
        embed = discord.Embed(
            title=f"{random.choice(greetings)}, {str(member)}!",
            description="\n".join(channel_mentions),
            color=discord.Color.from_rgb(84,74,165)
        )

        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_author(name=str(member),
                         icon_url=self.bot.user.display_avatar.url)

        await welcome_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        goodbye_messages = self.fetch_json("welcome.json").get("farewell")
        farewell_channel = next((channel for channel in member.guild.text_channels if channel.name in [
                                "farewell", "goodbye"]), None)
        id_role = next((role for role in member.roles if re.match(r'^>.*<$', role.name)), None)
        bureau_role = next((role for role in member.roles if re.match(r"^\[.*\]$", role.name)), None)

        if id_role and len(id_role.members) < 1:
            await id_role.delete()
                    
        if bureau_role and len(bureau_role.members) < 1:
            await bureau_role.delete()

        if farewell_channel is not None:
            embed = discord.Embed(
                title=f"{random.choice(goodbye_messages)} {str(member)} has left the server.",
                color=discord.Color.from_rgb(84,74,165)
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_author(name=str(member),
                             icon_url=self.bot.user.display_avatar.url)

            await farewell_channel.send(embed=embed)

    #todo fix nexttime
    @commands.command(aliases=["neomi"])
    async def introduce(self, ctx):
        embed = discord.Embed(
            title="_Neomi_ Dayo ૮ ˶ᵔ ᵕ ᵔ˶ ა ~ !",
            description="Hello there! I'm your friendly and charming bot here to spread joy and bring smiles to all!",
            color=ctx.author.color
        )
        embed.add_field(
            name="🌠 Purpose",
            value="My purpose is to brighten your day, provide helpful information, and make your Discord experience enjoyable!"
        )
        embed.add_field(
            name="🚀 Features",
            value="I have a variety of fun commands, mini-games, and useful utilities waiting for you to explore!"
        )
        embed.add_field(
            name="🔮 How to Interact",
            value="Just type my prefix followed by any command to get started. For example, try `./help` to see what I can do for you!"
        )
        embed.set_footer(
            text="Enjoy your time with me! Let's create unforgettable moments together."
        )

        await ctx.send(embed=embed)
    #todo fix nexttime
    @commands.command()
    async def cute(self, ctx):
        cute_messages = self.fetch_json("welcome.json").get("cute")
        cute_message = random.choice(cute_messages)
        await ctx.send(cute_message)

    # simulation of on_member_join, don't delete it my future self xd.
    # @commands.command()
    # async def member(self, ctx):
    #     greetings = self.fetch_json("welcome.json").get("greetings")

    #     role_channel = next((channel for channel in ctx.author.guild.text_channels if channel.name in ["role", "roles"]), None)
    #     rule_channel = next((channel for channel in ctx.author.guild.text_channels if channel.name in ["rule", "rules"]), None)

    #     channel_mentions = [f"• Get your roles at {role_channel.mention}", f"• Read the rules at {rule_channel.mention}"]
    #     embed = discord.Embed(
    #         title=f"{random.choice(greetings)}, {str(ctx.author)}!",
    #         description="\n".join(channel_mentions),
    #         color=discord.Color.from_rgb(198, 175, 165)
    #     )

    #     embed.set_thumbnail(url=ctx.author.display_avatar.url)
    #     embed.set_author(name=str(ctx.author), icon_url=self.bot.user.display_avatar.url)

    #     await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Welcome(bot))
