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

# -----------------ERROR EMBEDS---------------------
doesntExist = discord.Embed(title= "⚠️ Error", description= "That command doesn't exist!", color=0xFFFF00)
doesntExist.set_footer(text= "Type &commands to see all the commands!")
missingArguments = discord.Embed(title= "⚠️ Error", description= "You're missing some arguments!", color=0xFFFF00)
missingPermission = discord.Embed(title= "⚠️ Error", description= "You don't have permission to use this command!", color=0xFFFF00)
commandCooldown = discord.Embed(title= "⚠️ Error", description= "You're on cooldown!", color=0xFFFF00)

# -----------------COG EMBEDS---------------------
cogNotFound = discord.Embed(title= "⚠️ Error", description= "That cog doesn't exist!", color=0xFFFF00)
loadCog = discord.Embed(title= "✅ Success", description= "Cog loaded!", color=0x00FFD8)
unloadCog = discord.Embed(title= "✅ Success", description= "Cog unloaded!", color=0xA233FF)
reloadCog = discord.Embed(title= "✅ Success", description= "Cog reloaded!", color=0x00FFD8)
reloadAllCogs = discord.Embed(title= "✅ Success", description= "All cogs reloaded!", color=0x00FFD8)

#Bot wide error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(embed=doesntExist)

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=missingArguments)

    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=missingPermission)

    elif isinstance(error, commands.CheckFailure):
        await ctx.send(embed=missingPermission)

    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(embed=commandCooldown)
        
    else:
        raise error

#Cog loading/Unloading
@bot.command(name= "load")
@commands.has_role("Botman")
async def _load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    console.log("[bright_cyan]{extension} has been loaded[/bright_cyan]".format(extension= extension.capitalize()))
    await ctx.send(embed=loadCog)

@bot.command(name= "unload")
@commands.has_role("Botman")
async def _unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    console.log("[bright_magenta]{extension} Cog unloaded...[/bright_magenta]".format(extension= extension.capitalize()))
    await ctx.send(embed=unloadCog)

@bot.command(name= "reload")
@commands.has_role("Botman")
async def _reload(ctx, extension):    
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(embed=reloadCog)

@bot.command(name= "reloadall")
@commands.has_role("Botman")
async def _reloadall(ctx):
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            bot.unload_extension(f'cogs.{file[:-3]}')
            console.log("[bright_magenta]{extension} Cog unloaded...[/bright_magenta]".format(extension= file[:-3].capitalize()))
            bot.load_extension(f'cogs.{file[:-3]}')
            console.log("[bright_cyan]{extension} Cog loaded...[/bright_cyan]".format(extension= file[:-3].capitalize()))
    
    await ctx.send(embed=reloadAllCogs)

#Load all cogs on startup
for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')
        console.log("[bright_cyan]{extension} Cog loaded...[/bright_cyan]".format(extension= file[:-3].capitalize()))
        
bot.run(os.getenv('BOT_TOKEN')) #runs bot