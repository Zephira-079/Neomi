import discord
from discord.ext import commands

#NOTICE prohibited to public (discordMember)
#TODO move this somewhere or rename it to a good name
class RoleButton(discord.ui.Button):
    def __init__(self, role_name):
        super().__init__(label=role_name, style=discord.ButtonStyle.primary)
        self.role_name = role_name

    async def callback(self, interaction: discord.Interaction):
        member = interaction.guild.get_member(interaction.user.id)
        role = discord.utils.get(interaction.guild.roles, name=self.role_name)
        if role:
            if role in member.roles:
                await member.remove_roles(role)
                await interaction.response.send_message(f"Role '{self.role_name}' removed.", ephemeral=True)
            else:
                await member.add_roles(role)
                await interaction.response.send_message(f"Role '{self.role_name}' added.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Role '{self.role_name}' not found. Please contact an administrator.", ephemeral=True)

