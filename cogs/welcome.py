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
            color=discord.Color.from_rgb(198, 175, 165)
        )

        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_author(name=str(member),
                         icon_url=self.bot.user.display_avatar.url)

        await welcome_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        goodbye_messages = [
            "Farewell!", "Goodbye!", "Until we meet again!", "Take care!", "See you later!",
            "Goodbye and good luck!", "Stay safe!", "We'll miss you!", "Adios!", "Au revoir!",
            "Auf Wiedersehen!", "Arrivederci!", "Sayonara!", "Annyeong!", "Zai jian!",
            "Namaste!", "Khuda hafiz!", "Do svidaniya!", "La revedere!"
        ]
        farewell_channel = next((channel for channel in member.guild.text_channels if channel.name in [
                                "farewell", "goodbye"]), None)

        if farewell_channel is not None:
            embed = discord.Embed(
                title=f"{random.choice(goodbye_messages)} {str(member)} has left the server.",
                color=discord.Color.from_rgb(198, 175, 165)
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_author(name=str(member),
                             icon_url=self.bot.user.display_avatar.url)

            await farewell_channel.send(embed=embed)

    #todo fix nexttime
    @commands.command()
    async def introduce(self, ctx):
        embed = discord.Embed(
            title="🌟 Cute Bot Introduction 🌟",
            description="Hello there! I'm your friendly and adorable bot here to spread cuteness and joy!",
            color=self.bot.user.color
        )
        embed.add_field(
            name="🌸 Purpose",
            value="My purpose is to bring smiles, provide helpful information, and make your day brighter!"
        )
        embed.add_field(
            name="✨ Features",
            value="I have a variety of fun commands, mini-games, and cute utilities waiting for you to explore!"
        )
        embed.add_field(
            name="🌈 How to Interact",
            value="Just type my prefix followed by any command to get started. For example, try `./cute` for a dose of cuteness!"
        )
        embed.set_footer(
            text="Enjoy your time with me! Let's create memorable moments together.")

        await ctx.send(embed=embed)
    #todo fix nexttime
    @commands.command()
    async def cute(self, ctx):
        cute_messages = [
            "You're as cute as a button!",
            "You're a ray of sunshine in a cloudy day!",
            "You bring smiles wherever you go!",
            "You're like a fluffy cloud of happiness!",
            "You have the cutest smile ever!",
            "You're a precious gem shining brightly!",
            "You make the world a more adorable place!",
            "You're sweeter than a candy!",
            "You're the definition of cuteness overload!",
            "You're the cutest bean in the garden of life!"
        ]
        cute_message = random.choice(cute_messages)
        await ctx.send(cute_message)

    # simulation of on_member_join, don't delete it my future self xd.
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
