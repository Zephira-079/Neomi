from discord.ext import commands
import discord
import requests
import random
import asyncio
from bs4 import BeautifulSoup
from googletrans import Translator

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
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
            title='_"Quote"_', description=text, color=discord.Color.from_rgb(198, 175, 165)
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
        await ctx.send(id)

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
    
    @commands.command(aliases=["rename","name"])
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

    @commands.command(aliases=["nyah","nya","nyeow","meow","nyahn","nyan","mew","purr","whatdacatdoin"])
    async def cat(self, ctx):
        response = requests.get('https://api.thecatapi.com/v1/images/search')
        if response.status_code == 200:
            data = response.json()
            image_url = data[0]['url']

            embed = discord.Embed(title="Neo'w! ~ 💕^^", color=discord.Color.from_rgb(230, 230, 230))
            embed.set_image(url=image_url)

            await ctx.send(embed=embed)
        else:
            await ctx.send("Failed to fetch a cat image. Try again later.")

    @commands.command()
    async def poll(self, ctx, question, *options):
        if len(options) < 2 or len(options) > 10:
            await ctx.send("Please provide at least 2 options and no more than 10 options.")
            return
        # Create the poll embed
        embed = discord.Embed(title="Poll", description=question, color=discord.Color.from_rgb(198, 175, 165))
        # Add options as fields
        for i, option in enumerate(options):
            emoji = chr(0x1f1e6 + i)  # Using regional indicator symbols as emojis
            embed.add_field(name=f"{emoji} Option {i+1}", value=option, inline=False)
        poll_message = await ctx.send(embed=embed)
        # Add reactions to the poll message for each option
        for i in range(len(options)):
            emoji = chr(0x1f1e6 + i)
            await poll_message.add_reaction(emoji)
    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please provide a question and at least 2 options.")

    # todo fix
    # @commands.command()
    # async def translate(self, ctx, target_lang, *, text):
    #     translation = self.translator.translate(text, dest=target_lang)
    #     source_lang = translation.src
    #     translated_text = translation.text

    #     embed = discord.Embed(
    #         title="Translation",
    #         description=f"Translated from {source_lang} to {target_lang}:",
    #         color=discord.Color.blue()
    #     )
    #     embed.add_field(name="Original Text", value=text, inline=False)
    #     embed.add_field(name="Translated Text", value=translated_text, inline=False)

    #     await ctx.send(embed=embed)
        
    # @commands.command()
    # async def meme(self, ctx):
    #     # Make a GET request to the meme API
    #     response = requests.get("https://api.example.com/memes")

    #     if response.status_code == 200:
    #         # Extract the meme data from the response
    #         meme_data = response.json()
    #         meme_url = meme_data["url"]
    #         meme_title = meme_data["title"]

    #         # Create an embed with the meme information
    #         embed = discord.Embed(
    #             title=meme_title,
    #             color=discord.Color.random()
    #         )
    #         embed.set_image(url=meme_url)

    #         # Send the meme as an embed
    #         await ctx.send(embed=embed)
    #     else:
    #         await ctx.send("Failed to fetch a meme. Please try again later.")

    #todo fix
    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title="User Information", color=member.color)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Name", value=member.name)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Status", value=member.status)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"))
        embed.add_field(name="Joined Discord", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"))
        embed.add_field(name="Roles", value=" ".join([role.mention for role in member.roles]))
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Basic(bot))