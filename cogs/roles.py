from discord.ext import commands
import discord
import asyncio
from emoji import emojize, emoji_count

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def react_message(self, ctx, emoji_name, message):
            custom_emoji = discord.utils.get(ctx.guild.emojis, name=emoji_name)
            emoji_unicode = emojize(f":{emoji_name}:", use_aliases=True)
            if bool(emoji_count(emoji_name)):
                await message.add_reaction(emoji_name)
            elif custom_emoji:
                emoji_format = f"<:{custom_emoji.name}:{custom_emoji.id}>"
                await message.add_reaction(emoji_format)
            elif emoji_unicode:
                await message.add_reaction(emoji_unicode)
            else:
                await message.add_reaction("❔")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)
        channel = guild.get_channel(payload.channel_id)
        # message = await channel.fetch_message(payload.message_id)

        role_channel = next((channel for channel in user.guild.text_channels if channel.name in [
                               "role", "roles"]), None)
            
        data_message = [message.embeds[0].to_dict() async for message in role_channel.history(limit=None)]
        
        print(data_message[0])

        # for reaction in reactions:
        #     async for user in reaction.users():
        #         print(f'Reaction {reaction.emoji} added by {user.name}')

        # if payload.message_id == 1121581559695278292 and payload.user_id != self.bot.user.id:
        #     pass

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

    # getting channel history/messages
    
    # @commands.command()
    # async def get(self, ctx):
    #     channel_name = "role"

    #     for guild in self.bot.guilds:
    #         channel = discord.utils.get(guild.text_channels, name=channel_name)
            
    #         if channel:
    #             messages = await channel.history(limit=None).flatten()

    #             for message in messages:
    #                 print(message.content)
    #             break  # Exit the loop if the channel is found
    #     if not channel:
    #         print(f"Channel '{channel_name}' not found.")



async def setup(bot):
    await bot.add_cog(Roles(bot))