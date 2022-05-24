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
#Bot statuses
@bot.event
async def on_connect():
    console.log("[green]Connected to discord's servers[/Green]")

@bot.event
async def on_disconnect():
    console.log("[red]Disconnected from discord's servers[/red]")

@bot.event
async def on_resumed():
    console.log("[green]Resumed connection to discord's servers[/green]")

@bot.event
async def on_ready():
    console.log("[green]Logged in as {0.user}[/green]".format(bot))
    await bot.change_presence(activity= discord.Game(name= "&commands")) #sets bot's status

#General Events
@bot.event
async def on_member_join(member):
    console.print("[green]{0.name} has joined the server[/green]".format(member))
    await member.send("Welcome {0.mention} to the server!".format(member))
    await member.send("Type '&commands' to see a list of commands!")

@bot.event
async def on_member_remove(member):
    console.print("[red]{0.name} has left the server[/red]".format(member))
    await member.send("Goodbye {0.mention}! Hope to see you again!".format(member))

#Admin Events
@bot.event
async def on_member_ban(guild, member):
    console.print("[red]{0.name} has been banned[/red]".format(member))
    await member.send("You have been banned from the server!")

@bot.event
async def on_member_unban(guild, member):
    console.print("[green]{0.name} has been unbanned[/green]".format(member))
    await member.send("You have been unbanned from the server!")

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
        await ctx.send("Downloading your video")
        await ctx.send("Downloaded {0}".format(ctx.message.author.mention), file= discord.File("videos/video.mp4")) #sends video to channel

bot.run(config['token'])