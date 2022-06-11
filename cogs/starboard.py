import sys
sys.dont_write_bytecode = True #Prevents creation of .pyc files
import discord
from discord.ext import commands
from discord.utils import get
import random

class Starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.starboard = bot.get_channel(984637437882036314)
        self.colors = [0xFF0000, 0xFF7F00, 0xFFFF00, 0x00FF00, 0x00FFFF, 0x0000FF, 0xFF00FF, 0xFAFAFA]

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.emoji.name == "⭐":
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            member = payload.member
            reaction = get(message.reactions, emoji=payload.emoji.name)

            if reaction and reaction.count >= 4:
                starboardEmbed = discord.Embed(title=f"{message.author}", description=f"{message.content}", color=random.choice(self.colors))
                starboardEmbed.set_image(url=message.attachments[0].url)
                await self.starboard.send(embed=starboardEmbed)

def setup(bot):
    bot.add_cog(Starboard(bot))