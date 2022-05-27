import sys
sys.dont_write_bytecode = True #Prevents creation of .pyc files
import discord
from discord.ext import commands
from rich.console import Console

console = Console() #Rich console

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Events
    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        console.log("[purple]{0} has been banned[/purple]".format(member))
        
        #exception handling
        try:
            await member.send("You have been banned from the server!")

        except discord.errors.Forbidden: #if user has DMs disabled
            pass

    @commands.Cog.listener()
    async def on_member_unban(self, guild, member):
        console.log("[yellow]{0} has been unbanned[/yellow]".format(member))
        
        #exception handling
        try:
            await member.send("You have been unbanned from the server!")

        except discord.errors.Forbidden: #if user has DMs disabled
            pass

    #Commands
    @commands.command(name= "ban")
    @commands.has_permissions(ban_members= True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send("{0} has been banned!".format(member))

    @commands.command(name= "unban")
    @commands.has_permissions(ban_members= True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                return

    @commands.command(name= "kick")
    @commands.has_permissions(kick_members= True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send("{0} has been kicked!".format(member))

#Cog setup
def setup(bot):
    bot.add_cog(Moderation(bot))
    console.log("[bright_cyan]Moderation Cog loaded...[/bright_cyan]")