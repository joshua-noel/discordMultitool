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
        #exception handling
        try:
            await member.send("You have been banned from {0}".format(guild.name))

        except discord.errors.Forbidden: #if user has DMs disabled
            pass

    @commands.Cog.listener()
    async def on_member_unban(self, guild, member):
        #exception handling
        try:
            await member.send("You have been unbanned from {0}".format(guild.name))

        except discord.errors.Forbidden: #if user has DMs disabled
            pass

    #Commands
    @commands.command(name= "ban")
    @commands.has_permissions(ban_members=True)
    #@commands.has_role("Admin")
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send("{0} has been banned!".format(member))

    @commands.command(name= "unban")
    @commands.has_permissions(ban_members=True)
    #@commands.has_role("Admin")
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                return

    @commands.command(name= "kick")
    @commands.has_permissions(kick_members=True)
    #@commands.has_any_role("Admin", "Moderator")
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send("{0} has been kicked!".format(member))

    @commands.command(name= "warn")
    @commands.has_permissions(kick_members=True)
    #@commands.has_any_role("Admin", "Moderator")
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        await member.send("You have been warned in {0} for {1}".format(ctx.guild.name, reason))
        await ctx.send("{0} has been warned!".format(member))

class Tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name= "newtext")
    @commands.has_permissions(manage_channels=True)
    async def createchannel(self, ctx, channel_name, category= None):
        if category == None:
            await ctx.guild.create_text_channel(channel_name)

        else:
            category = discord.utils.get(ctx.guild.categories, name=category)
            await ctx.guild.create_text_channel(channel_name, category=category)

    @commands.command(name= "newvc")
    @commands.has_permissions(manage_channels=True)
    async def createvc(self, ctx, channel_name, category= None):
        if category == None:
            await ctx.guild.create_voice_channel(channel_name)

        else:
            category = discord.utils.get(ctx.guild.categories, name=category)
            await ctx.guild.create_voice_channel(channel_name, category=category)

    @commands.command(name= "newcategory")
    @commands.has_permissions(manage_channels=True)
    async def createcat(self, ctx, category_name):
        await ctx.guild.create_category(category_name)

    @commands.command(name= "renametext")
    @commands.has_permissions(manage_channels=True)
    async def renamechannel(self, ctx, original, new):
        channel = discord.utils.get(ctx.guild.channels, name=original)
        await channel.edit(name=new)
        await ctx.send("{0} has been renamed to {1}!".format(original, new))

    @commands.command(name= "renamevc")
    @commands.has_permissions(manage_channels=True)
    async def renamevc(self, ctx, original, new):
        channel = discord.utils.get(ctx.guild.channels, name=original)
        await channel.edit(name=new)
        await ctx.send("{0} has been renamed to {1}!".format(original, new))

    @commands.command(name= "renamecategory", aliases= ["renamecat"])
    @commands.has_permissions(manage_channels=True)
    async def renamecat(self, ctx, original, new):
        category = discord.utils.get(ctx.guild.categories, name=original)
        await category.edit(name=new)
        await ctx.send("{0} has been renamed to {1}!".format(original, new))

    @commands.command(name= "delete")
    @commands.has_permissions(manage_channels=True)
    async def deletechannel(self, ctx, channel_name):
        channel = discord.utils.get(ctx.guild.channels, name=channel_name)
        await channel.delete()
        await ctx.send("{0} has been deleted!".format(channel_name))

    @commands.command(name= "deletecategory", aliases=["deletecat"])
    @commands.has_permissions(manage_channels=True)
    async def deletecat(self, ctx, category_name):
        category = discord.utils.get(ctx.guild.categories, name=category_name)
        await category.delete()
        await ctx.send("{0} has been deleted!".format(category_name))

def setup(bot):
    bot.add_cog(Moderation(bot))
    bot.add_cog(Tools(bot))