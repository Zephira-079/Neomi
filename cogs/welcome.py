from discord.ext import commands
import discord
import random

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        greetings = [
            "Hello!", "Hi there!", "Welcome!", "Greetings!", "Good to see you!",
            "Howdy!", "Salutations!", "Hey!", "Nice to meet you!", "Hola!",
            "Bonjour!", "Guten Tag!", "Ciao!", "Namaste!", "Salaam!",
            "Konnichiwa!", "Annyeonghaseyo!", "Merhaba!", "Zdravstvuyte!",
            "Privet!"
        ]
        welcome_channel = next((channel for channel in member.guild.text_channels if channel.name in ["greetings","welcome"]), None)

        role_channel = next((channel for channel in member.guild.text_channels if channel.name in ["role", "roles"]), None)
        rule_channel = next((channel for channel in member.guild.text_channels if channel.name in ["rule", "rules"]), None)

        channel_mentions = [f"• Get your roles at {role_channel.mention}", f"• Read the rules at {rule_channel.mention}"]
        embed = discord.Embed(
            title=f"{random.choice(greetings)}, {str(member)}!",
            description="\n".join(channel_mentions),
            color=discord.Color.from_rgb(198, 175, 165)
        )

        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_author(name=str(member), icon_url=self.bot.user.display_avatar.url)

        await welcome_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        goodbye_messages = [
            "Farewell!", "Goodbye!", "Until we meet again!", "Take care!", "See you later!",
            "Goodbye and good luck!", "Stay safe!", "We'll miss you!", "Adios!", "Au revoir!",
            "Auf Wiedersehen!", "Arrivederci!", "Sayonara!", "Annyeong!", "Zai jian!",
            "Namaste!", "Khuda hafiz!", "Do svidaniya!", "La revedere!"
        ]
        farewell_channel = next((channel for channel in member.guild.text_channels if channel.name in ["farewell", "goodbye"]), None)
        
        if farewell_channel is not None:
            embed = discord.Embed(
                title=f"{random.choice(goodbye_messages)} {str(member)} has left the server.",
                color=discord.Color.from_rgb(198, 175, 165)
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_author(name=str(member), icon_url=self.bot.user.display_avatar.url)

            await farewell_channel.send(embed=embed)

    # @commands.command()
    # async def member(self, ctx):
    #     greetings = [
    #         "Hello!", "Hi there!", "Welcome!", "Greetings!", "Good to see you!",
    #         "Howdy!", "Salutations!", "Hey!", "Nice to meet you!", "Hola!",
    #         "Bonjour!", "Guten Tag!", "Ciao!", "Namaste!", "Salaam!",
    #         "Konnichiwa!", "Annyeonghaseyo!", "Merhaba!", "Zdravstvuyte!",
    #         "Privet!"
    #     ]

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
