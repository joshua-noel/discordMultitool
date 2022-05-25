#!/usr/bin/env python
import discord
from discord.ext import commands
import json
import os

#Setup
#loads config
with open("config.json", "r") as f:
    config = json.load(f)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix= config["prefix"], intents=intents)

#Cog loading/Unloading
@bot.command
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

@bot.command(name= "reload")
async def _reload(ctx, extension):    
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')

@bot.command(name= "reloadAll")
async def reloadAll(ctx):
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            bot.unload_extension(f'cogs.{file[:-3]}')
            bot.load_extension(f'cogs.{file[:-3]}')

#Load all cogs on startup
for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')
        
bot.run(config['token'])