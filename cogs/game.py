from discord.ext import commands
import discord
import asyncio
import random

class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # russianroulette
    @commands.command(aliases=["rr"])
    async def russianroulette(self, ctx, *members: discord.Member):
        self.participants = list(members)
        confirmations = []

        embed = discord.Embed(
            title="Russian Roulette Begins!",
            description="- The mentioned participants must respond with either **Yes/y** or **No/n** to confirm their decision to join. Once they make their choice, there is no option to change it.\n- The rules are straightforward: When the command \"./rollsgun\" is invoked, prepare yourself for what's to come.",
            color=discord.Color.from_rgb(84, 74, 165)
        )

        await ctx.send(embed=embed)
        await asyncio.sleep(1)

        for member in members:
            if member.bot:
                await ctx.send("Bots are prohibited from joining the game!!!")
                continue
            elif member == ctx.guild.owner:
                await ctx.send("Owner are prohibited from joining the game!!!")
                continue
            elif member in confirmations:
                await ctx.send(f"{member.mention} has already joined the game!!!")
                continue
            await ctx.send(f"{member.mention}, Do you want to join the Russian Roulette? (yes/no)")

            def check(message):
                return message.author == member and message.channel == ctx.channel

            try:
                confirmation = await self.bot.wait_for('message', timeout=7, check=check)
            except asyncio.TimeoutError:
                await ctx.send(f"{member.mention}, You didn't respond in time. You're not included in the game.")
                continue

            if confirmation.content.lower().strip() in ["yes", "y", "true", "maybe", "probably", "possibly", "1"]:
                confirmations.append(member)
                await ctx.send(f"{member.mention}, You're actively participating now! There's no turning back!")
            else:
                await ctx.send(f"{member.mention}, You're not included in the game.")

        self.participants = confirmations

    @commands.command(aliases=["rrfire","spincy","rollsgun","firegun"])
    async def spincylinder(self, ctx):
        if len(self.participants) < 1:
            await ctx.send("No participants found.")
            return
        elif len(self.participants) == 1:
            await ctx.send(f"Not enough participants")
            return

        await asyncio.sleep(.5)
        await ctx.send("Rolling the gun...")
        await asyncio.sleep(random.randint(2, 7))
        await ctx.send("Fire!!! 🔥")
        await asyncio.sleep(.5)

        chosen = random.choice(self.participants)
        self.participants.remove(chosen)

        await ctx.send(f"{chosen.mention} has been chosen! They are kicked from the server!")
        await chosen.kick()
        if len(self.participants) == 1:
            await ctx.send(f"{self.participants[0]} Phew!!!,Lucky You Survive!!!")
            self.participants.pop()

async def setup(bot):
    await bot.add_cog(Game(bot))