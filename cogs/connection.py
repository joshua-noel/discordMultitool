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
        console.log("[green]Connected to discord's servers[/green]")

    @commands.Cog.listener()
    async def on_disconnect(self):
        console.log("[yellow]Disconnected from discord's servers[/yellow]")

    @commands.Cog.listener()
    async def on_resumed(self):
        console.log("[green]Resumed connection to discord's servers[/green]")

    @commands.Cog.listener()
    async def on_ready(self):
        console.log("[green]Logged in as {0.user}[/green]".format(self.bot))
        await self.bot.change_presence(activity= discord.Game(name= "&help")) #sets bot's status

        #establish database connection
        async with aiosqlite.connect('database.db') as db:
            console.log("[blue]Economy database connection established[/blue]")
            #database creation
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS economy (user_id INTEGER PRIMARY KEY, server_id INTEGER, balance INTEGER DEFAULT 500)")
            
            await db.commit() #commit changes

        async with aiosqlite.connect('levels.db') as db:
            console.log("[blue]Levels database connection established[/blue]")
            #database creation
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS levels (user_id INTEGER PRIMARY KEY, exp INTEGER, level INTEGER DEFAULT 1)")

            await db.commit() #commit changes

        async with aiosqlite.connect('elo.db') as db:
            console.log("[blue]Elo database connection established[/blue]")
            #database creation
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS elo (user_id INTEGER PRIMARY KEY, elo INTEGER DEFAULT 1000, wins INTEGER DEFAULT 0, losses INTEGER DEFAULT 0)")

            await db.commit()

#Cog setup
def setup(bot):
    bot.add_cog(Connection(bot))