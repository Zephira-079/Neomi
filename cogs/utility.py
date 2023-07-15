import discord
import json
from emoji import emojize, emoji_count

class Utility:
    def __init__(self):
        self.resource = "./assets/json/resource_cogs"
    
    def fetch_json(self, path):
        with open(f"{self.resource}/{path}", 'r') as file:
            return json.load(file)
        
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

    def emoji_translator(self, ctx, emoji_name):
        custom_emoji = discord.utils.get(ctx.guild.emojis, name=emoji_name)
        emoji_unicode = emojize(f":{emoji_name}:", use_aliases=True)
        if bool(emoji_count(emoji_name)):
            return emoji_name
        elif custom_emoji:
            emoji_format = f"<:{custom_emoji.name}:{custom_emoji.id}>"
            return emoji_format
        elif emoji_unicode:
            return emoji_unicode
        else:
            return "❔"
        
    async def edit_member_roles(self, member: discord.Member, *roles_to_assign):
        guild_roles = member.guild.roles
        roles = []

        for role_name in roles_to_assign:
            role = discord.utils.get(guild_roles, name=role_name)
            if role is not None:
                roles.append(role)
            else:
                role = await member.guild.create_role(name=role_name)
                roles.append(role)

        await member.edit(roles=roles)
