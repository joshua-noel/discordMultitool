#!/usr/bin/env python
import discord
import json
from colorama import init, Fore, Style
from YTDownloader import Download

#Setup
with open("token.json", "r") as f:
    token = json.load(f)

init() #Initialize colorama
client = discord.Client()

@client.event
async def on_connect():
    print(Fore.GREEN + "Connected to discord's servers" + Style.RESET_ALL)

@client.event
async def on_disconnect():
    print(Fore.RED + "Disconnected from discord's servers" + Style.RESET_ALL)

@client.event
async def on_ready():
    print(Fore.GREEN + "Logged in as {0.user}".format(client) + Style.RESET_ALL)

#Commands
async def commands(message):
    with open("commands.txt", "r") as f:
        commands = f.read().splitlines()
        await message.channel.send("```{0}```".format("\n".join(commands)))

async def download(message):
    pass
    #await message.channel.send(file= discord.File("videos/video.mp4"))

async def repeat(message):
    await message.channel.send("@{0} said {1}".format(message.author, message.content[7:]))

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
