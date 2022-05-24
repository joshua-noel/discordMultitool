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
        console.print("[red]{0.name} has been banned[/red]".format(member))
        await member.send("You have been banned from the server!")

    @commands.Cog.listener()
    async def on_member_unban(self, guild, member):
        console.print("[green]{0.name} has been unbanned[/green]".format(member))
        await member.send("You have been unbanned from the server!")

#Cog setup
def setup(bot):
    bot.add_cog(Moderation(bot))
    console.log("[green]Moderation Cog loaded...[/green]")