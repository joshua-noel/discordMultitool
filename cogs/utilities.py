import sys
sys.dont_write_bytecode = True #Prevents creation of .pyc files
import discord
from discord.ext import commands
from rich.console import Console
import YTDownloader as YT

console = Console() #Rich console

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name= "commands")
    async def _commands(self, ctx):
        embed = discord.Embed(title= "Commands", color= 0x00ff00)
        with open("commands.txt", "r") as f:
            commands = f.read().splitlines()

        for i in range(len(commands)):
            embed.add_field(name= f"{i+1}. {commands[i]}", value= "-------------------------------", inline=False)

        await ctx.send(embed=embed)

    """
    @commands.command(name= "download")
    async def download(self, ctx, url):
        await ctx.message.delete(delay= None) #deletes command message
        await ctx.send("Attempting to download your video {0}".format(ctx.message.author.mention), delete_after= 5.0) #limits channel spam

        if YT.Downloader().download(url) == 0: #downloads video
            await ctx.send("Could not download video {0}".format(ctx.message.author.mention))
            
        else:
            #upload size limit exception handling
            try:
                await ctx.send("Downloaded {0}".format(ctx.message.author.mention), file= discord.File("videos/video.mp4")) #sends video to channel

            except discord.errors.HTTPException:
                await ctx.send("Could not send video {0}".format(ctx.message.author.mention))
                console.log("[red]Could not send video {0}[/red]".format(ctx.message.author.mention))
    """

def setup(bot):
    bot.add_cog(Utilities(bot))
    console.log("[bright_cyan]Utilities Cog loaded...[/bright_cyan]")