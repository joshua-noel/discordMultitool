#!/usr/bin/env python
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

#Setup
load_dotenv() #Loads the .env file

intents = discord.Intents.all()
bot = commands.Bot(command_prefix= "&", intents=intents)

#Cog loading/Unloading
@bot.command
@commands.has_permissions(administrator= True)
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command
@commands.has_permissions(administrator= True)
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

@bot.command(name= "reload")
@commands.has_permissions(administrator= True)
async def _reload(ctx, extension):    
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')

@bot.command
@commands.has_permissions(administrator= True)
async def reloadall(ctx):
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            bot.unload_extension(f'cogs.{file[:-3]}')
            bot.load_extension(f'cogs.{file[:-3]}')

#Load all cogs on startup
for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')
        
bot.run(os.getenv('BOT_TOKEN')) #runs bot