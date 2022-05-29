import sys
sys.dont_write_bytecode = True #Prevents creation of .pyc files
import discord
from discord.ext import commands, tasks
import aiosqlite
from rich.console import Console

console = Console() #Rich console

class Leaderboard(commands.Cog):
    def __init__ (self, bot):
        self.bot = bot

    @commands.command(name= "global", aliases= ["gb"])
    async def _global(self, ctx):
        async with aiosqlite.connect('database.db') as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT user_id, balance FROM economy ORDER BY balance DESC") #Sorts by highest balance
                leaderboard = await cursor.fetchmany(10) #Gets top 10
                embed = discord.Embed(title= "Global Leaderboard", color= 0x00ff00) #Creates embed

                for i in range(len(leaderboard)):
                    user = self.bot.get_user(leaderboard[i][0]) #Gets user from user_id
                    embed.add_field(name= f"{i+1}. {user.name}", value= f"${leaderboard[i][2]}", inline=False)

                await ctx.send(embed=embed)
            
            await db.commit()

    @commands.command(name= "leaderboard", aliases= ["lb"])
    async def leaderboard(self, ctx):
        async with aiosqlite.connect('database.db') as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT user_id, balance FROM economy WHERE server_id = ? ORDER BY balance DESC", (ctx.guild.id,)) #Sorts by highest balance
                leaderboard = await cursor.fetchmany(10) #Gets top 10
                embed = discord.Embed(title= f"{ctx.guild.name} Leaderboard", color= 0x00ff00) #Creates embed
                
                for i in range(len(leaderboard)):
                    user = self.bot.get_user(leaderboard[i][0])
                    embed.add_field(name= f"{i+1}. {user.name}", value= f"${leaderboard[i][2]}", inline=False)

                await ctx.send(embed=embed)

            await db.commit()

def setup(bot):
    bot.add_cog(Leaderboard(bot))
    console.log("[bright_cyan]Leaderboard Cog loaded...[/bright_cyan]")
