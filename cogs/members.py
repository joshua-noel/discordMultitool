import sys
sys.dont_write_bytecode = True #Prevents creation of .pyc files
import discord
from discord.ext import commands
from rich.console import Console

console = Console() #Rich console

class Members(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.get_channel(978429063557431306)
        console.print("[green]{0.name} has joined the server[/green]".format(member))
        if channel is not None:
            await channel.send("Welcome to the server {0.mention}".format(member))

        await member.send("Welcome {0.mention} to the server!".format(member))
        await member.send("Type '&commands' to see a list of commands!")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = member.guild.get_channel(978429063557431306)
        console.print("[red]{0.name} has left the server[/red]".format(member))
        if channel is not None:
            await channel.send("@{0.name} has left the server".format(member))
            
        await member.send("Goodbye {0.mention}! Hope to see you again!".format(member))

def setup(bot):
    bot.add_cog(Members(bot))
    console.log("[green]Members Cog loaded...[/green]")
