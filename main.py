#!/usr/bin/env python
import discord
import json
from rich.console import Console
import YTDownloader as YT

#Setup
with open("token.json", "r") as f:
    token = json.load(f)

console = Console() #rich console object
client = discord.Client() #initalize discord bot

@client.event
async def on_connect():
    console.log("[green]Connected to discord's servers[/Green]")

@client.event
async def on_disconnect():
    console.log("[red]Disconnected from discord's servers[/red]")

@client.event
async def on_ready():
    console.log("[green]Logged in as {0.user}[/green]".format(client))

#Commands
#List commands
async def commands(message):
    with open("commands.txt", "r") as f:
        commands = f.read().splitlines()
        await message.channel.send("```{0}```".format("\n".join(commands)))

#Download YT video
async def download(message):
    url = message.content[10:] #gets url from message
    await message.delete(delay= None) #deletes command message

    if YT.Downloader().download(url) == 0: #downloads video
       await message.channel.send("Could not download video {0}".format(message.author.mention))
        
    else:
        await message.channel.send("Downloaded {0}".format(message.author.mention), file= discord.File("videos/video.mp4")) #sends video to channel

#Repeat user message
async def repeat(message):
    await message.channel.send("{0} said {1}".format(message.author.mention, message.content[7:]))

#Command handling
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("&commands"):
        await commands(message)

    if message.content.startswith("&download"):
        await download(message)

    if message.content.startswith("&repeat"):
        await repeat(message)

client.run(token['token'])
