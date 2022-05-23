#!/usr/bin/env python
import discord
from discord.ext import commands
import json
from rich.console import Console
import YTDownloader as YT

#Setup
#loads config
with open("config.json", "r") as f:
    config = json.load(f)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix= config["prefix"], intents=intents)

console = Console() #rich console object

#Events
@bot.event
async def on_connect():
    console.log("[green]Connected to discord's servers[/Green]")

@bot.event
async def on_disconnect():
    console.log("[red]Disconnected from discord's servers[/red]")

@bot.event
async def on_ready():
    console.log("[green]Logged in as {0.user}[/green]".format(bot))

#Commands
#List commands
@bot.command(name= "commands")
async def commands(ctx):
    with open("commands.txt", "r") as f:
        commands = f.read().splitlines()
        await ctx.send("```{0}```".format("\n".join(commands)))   

#Download YT video
@bot.command(name= "download")
async def download(ctx, url):
    await ctx.message.delete(delay= None) #deletes command message

    if YT.Downloader().download(url) == 0: #downloads video
        await ctx.send("Could not download video {0}".format(ctx.message.author.mention))
        
    else:
        await ctx.send("Downloaded {0}".format(ctx.message.author.mention), file= discord.File("videos/video.mp4")) #sends video to channel

bot.run(config['token'])
