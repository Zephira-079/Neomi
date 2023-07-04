from discord.ext import commands
import discord
import requests
import random
import asyncio
from bs4 import BeautifulSoup
import datetime
from cogs.utility import Utility


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.react_message = Utility().react_message
        self.fetch_json = Utility().fetch_json
    
    @commands.command(aliases=["h"])
    async def help(self, ctx):
        details = self.fetch_json("help.json")
        embed = discord.Embed(title="Definitely Commands", color=ctx.author.color)
        embed.set_author(name=details.get("title").format(ctx.author.display_name))
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.set_footer(text="||------------ More commands in the future ~ ヾ(≧▽≦*)o ------------||")

        for category, commands in details["descriptions"].items():
            command_list = [f"\u3164``{command}`` - ``{description}``" for command, description in commands.items()]
            embed.add_field(name=category.capitalize(), value="\n".join(command_list), inline=False)

        await ctx.send(embed=embed)


    @commands.command()
    async def say(self, ctx, *args):
        await ctx.message.delete()
        await ctx.send(" ".join(args))

    @commands.command()
    async def quote(self, ctx):
        response = requests.get("https://type.fit/api/quotes")
        quotes = response.json()
        quote = quotes[random.randint(0, len(quotes) - 1)]
        text = quote["text"]
        author = quote["author"] or "Unknown"
        embed = discord.Embed(
            title='_"Quote"_', description=text, color=discord.Color.from_rgb(84,74,165)
        )
        embed.set_footer(text=f"~ {author}")
        await ctx.send(embed=embed)

    @commands.command(aliases=["ping", "latensy"])
    async def latency(self, ctx):
        latency = f"{round(self.bot.latency * 100)}ms"
        await ctx.send(latency)

    @commands.command(aliases=["guild_id"])
    async def server_id(self, ctx):
        id = ctx.guild.id
        await ctx.send(f"||{id}||")

    @commands.command()
    async def remind(self, ctx, hours, *args):
        message = ctx.message
        await message.delete()

        hours = float(hours)
        minutes = hours * 60
        seconds = hours * 60 * 60
        days = hours * 24

        await asyncio.sleep(seconds)
        if seconds < 60:
            await ctx.send(
                f'From {ctx.author.mention}! {round(seconds, 2)} seconds ago, {" ".join(args)}'
            )
        elif minutes < 60:
            await ctx.send(
                f'From {ctx.author.mention}! {round(minutes, 2)} minutes ago, {" ".join(args)}'
            )
        elif hours < 24:
            await ctx.send(
                f'From {ctx.author.mention}! {round(hours, 2)} hours ago, {" ".join(args)}'
            )
        elif days < hours * 7:
            await ctx.send(
                f'From {ctx.author.mention}! {round(days, 2)} days ago, {" ".join(args)}'
            )
        else:
            await ctx.send(f'From {ctx.author.mention}! several days ago, {" ".join(args)}')

    @commands.command()
    async def define(ctx, *words):
        words = " ".join(words)
        response = requests.get(f"https://www.dictionary.com/browse/{words}")
        soup = BeautifulSoup(response.content, "html.parser")
        definition_meta = soup.find("meta", {"name": "description"})

        try:
            definition = definition_meta["content"]
            await ctx.send(f"Definition of '{words}': {definition}")
        except TypeError:
            await ctx.send(f"Definition of '{words}' is not found")

    @commands.command(aliases=["rename", "name"])
    async def nickname(self, ctx, new_nickname):
        await ctx.message.delete()
        target_user = ctx.author

        try:
            await target_user.edit(nick=new_nickname)
        except discord.Forbidden:
            pass

    @commands.command()
    async def cursive(self, ctx, *, text):
        cursive_text = ""
        for char in text.lower():
            if char.isalpha():
                cursive_text += chr(ord(char) + 0x1D4D0 - ord('a'))
            else:
                cursive_text += char
        await ctx.send(cursive_text)

    @commands.command(aliases=["nyah", "nya", "nyeow", "meow", "nyahn", "nyan", "mew", "purr", "whatdacatdoin"])
    async def cat(self, ctx):
        response = requests.get('https://api.thecatapi.com/v1/images/search')
        if response.status_code == 200:
            data = response.json()
            image_url = data[0]['url']

            embed = discord.Embed(title="Neo'w! ~ 💕^^",
                                  color=discord.Color.from_rgb(84,74,165))
            embed.set_image(url=image_url)

            await ctx.send(embed=embed)
        else:
            await ctx.send("Failed to fetch a cat image. Try again later.")

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title="User Information", color=member.color)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Name", value=member.name)
        embed.add_field(name="ID", value=f"||{member.id}||")
        embed.add_field(name="Status", value=member.status)
        embed.add_field(name="Joined Server",
                        value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"))
        embed.add_field(name="Joined Discord",
                        value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"))
        embed.add_field(name="Roles", value=" ".join(
            [role.mention for role in member.roles]))
        await ctx.send(embed=embed)

    #moderation.
    
    @commands.command()
    async def report(self, ctx, *message):
        if not message:
            return
        #time
        current_time = datetime.datetime.utcnow()
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S UTC')

        text_channels = ctx.guild.text_channels
        report_channel = next((channel for channel in text_channels if channel.name in ["report", "reports"]), None)
        embed = discord.Embed(title=f"Report From {ctx.author}!", description=f"{' '.join(message)}", color=ctx.author.color)
        embed.set_footer(text=formatted_time)

        await report_channel.send(embed=embed)

    @commands.command(aliases=["suggest"])
    async def suggestion(self, ctx, *message):
        if not message:
            return
        #time
        current_time = datetime.datetime.utcnow()
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S UTC')

        text_channels = ctx.guild.text_channels
        report_channel = next((channel for channel in text_channels if channel.name in ["suggest", "suggestion", "suggestions"]), None)
        embed = discord.Embed(title=f"Report From {ctx.author}!", description=f"{' '.join(message)}", color=ctx.author.color)
        embed.set_footer(text=formatted_time)

        await report_channel.send(embed=embed)

    @commands.command(aliases=["poll"])
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
    await bot.add_cog(General(bot))
