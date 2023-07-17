from discord.ext import commands
import discord
from datetime import timedelta
from modules.utility import Utility

class Guardian(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.anti_spam = commands.CooldownMapping.from_cooldown(5, 15, commands.BucketType.member)
        self.too_many_violations = commands.CooldownMapping.from_cooldown(4, 60, commands.BucketType.member)
        self.edit_member_roles = Utility().edit_member_roles
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if type(message.channel) is not discord.TextChannel or message.author.bot: return
        bucket = self.anti_spam.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            await message.delete()
            await message.channel.send(f"{message.author.mention}, Don't spam!", delete_after = 10)
            violations = self.too_many_violations.get_bucket(message)
            check = violations.update_rate_limit()
            if check:
                await self.edit_member_roles(message.author, "Isolated") #"Isolated" # todo put somewhere in config files in future
                await message.author.timeout(timedelta(hours=12), reason = "Spamming")

async def setup(bot):
    await bot.add_cog(Guardian(bot))