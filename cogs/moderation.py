import sys
sys.dont_write_bytecode = True #Prevents creation of .pyc files
import discord
from discord.ext import commands
from rich.console import Console

console = Console() #Rich console

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        console.log("[purple]{0} has been banned[/purple]".format(member))
        
        #exception handling
        try:
            await member.send("You have been banned from the server!")

        except discord.errors.Forbidden: #if user has DMs disabled
            pass

    @commands.Cog.listener()
    async def on_member_unban(self, guild, member):
        console.log("[yellow]{0} has been unbanned[/yellow]".format(member))
        
        #exception handling
        try:
            await member.send("You have been unbanned from the server!")

        except discord.errors.Forbidden: #if user has DMs disabled
            pass

#Cog setup
def setup(bot):
    bot.add_cog(Moderation(bot))
    console.log("[bright_cyan]Moderation Cog loaded...[/bright_cyan]")