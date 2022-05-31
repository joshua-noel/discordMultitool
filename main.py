#!/usr/bin/env python
import discord
from discord.ext import commands
from rich.console import Console
from dotenv import load_dotenv
import os

#Setup
console = Console() #Rich console
load_dotenv() #Loads the .env file

intents = discord.Intents.all()
bot = commands.Bot(command_prefix= "&", intents=intents)

#Bot wide error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("That command doesn't exist!")

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You're missing a required argument!")

    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to do that!")

    elif isinstance(error, commands.CheckFailure):
        await ctx.send("You don't have permission to do that!")

    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send("You're on cooldown!")
        
    else:
        raise error

#Cog loading/Unloading
@bot.command(name= "load")
@commands.has_permissions(administrator= True)
async def _load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    console.log("[bright_cyan]{extension} has been loaded[/bright_cyan]".format(extension))

@bot.command(name= "unload")
@commands.has_permissions(administrator= True)
async def _unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    console.log("[bright_magenta]{extension} Cog unloaded...[/bright_magenta]".format(extension= extension.capitalize()))

@bot.command(name= "reload")
@commands.has_permissions(administrator= True)
async def _reload(ctx, extension):    
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')

@bot.command(name= "reloadall")
@commands.has_permissions(administrator= True)
async def _reloadall(ctx):
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            bot.unload_extension(f'cogs.{file[:-3]}')
            console.log("[bright_magenta]{extension} Cog unloaded...[/bright_magenta]".format(extension= file[:-3].capitalize()))
            bot.load_extension(f'cogs.{file[:-3]}')
            console.log("[bright_cyan]{extension} Cog loaded...[/bright_cyan]".format(extension= file[:-3].capitalize()))

#Load all cogs on startup
for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')
        console.log("[bright_cyan]{extension} Cog loaded...[/bright_cyan]".format(extension= file[:-3].capitalize()))
        
bot.run(os.getenv('BOT_TOKEN')) #runs bot