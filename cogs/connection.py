import sys
sys.dont_write_bytecode = True #Prevents creation of .pyc files
import discord
from discord.ext import commands
import aiosqlite
from rich.console import Console

console = Console() #Rich console

class Connection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_connect(self):
        console.log("[green]Connected to discord's servers[/Green]")

    @commands.Cog.listener()
    async def on_disconnect(self):
        console.log("[bright_magenta]Disconnected from discord's servers[/bright_magenta]")

    @commands.Cog.listener()
    async def on_resumed(self):
        console.log("[green]Resumed connection to discord's servers[/Green]")

    @commands.Cog.listener()
    async def on_ready(self):
        console.log("[green]Logged in as {0.user}[/green]".format(self.bot))
        await self.bot.change_presence(activity= discord.Game(name= "&commands")) #sets bot's status

        #establish database connection
        async with aiosqlite.connect('database.db') as db:
            console.log("[blue]Initial database connection established...[/blue]")
            #database creation
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS economy (user_id INTEGER PRIMARY KEY, balance INTEGER DEFAULT 500)")
            
            await db.commit() #commit changes

#Cog setup
def setup(bot):
    bot.add_cog(Connection(bot))
    console.log("[bright_cyan]Connection Cog loaded...[/bright_cyan]")