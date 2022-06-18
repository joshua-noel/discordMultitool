import sys
sys.dont_write_bytecode = True #Prevents creation of .pyc files
import discord
from discord.ext import commands
import asyncio
import aiosqlite
import math

class EloComputations():
    def __init__(self, bot):
        pass

    async def winProb(self, eloA, eloB):
        return 1 / (1 + math.pow(10, (eloB - eloA) / 400))

    async def computeElo(self, eloA, expectedA, outcome, k = 32):
        return eloA + k * (outcome - expectedA)

class Elo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def getElo(self, user):
        async with aiosqlite.connect('elo.db') as db:
            cursor = await db.execute("SELECT elo FROM elo WHERE user_id = ?", (user.id,))
            elo = await cursor.fetchone()

            if elo is None:
                await db.execute("INSERT INTO elo VALUES (?, ?, ?, ?)", (user.id, 1000, 0, 0))
                await db.commit()
                return 1000

            else:
                return elo[0]

    async def updateStats(self, personA, personB, outcome):
        eloA = await self.getElo(personA)
        eloB = await self.getElo(personB)

        expectedA = await EloComputations(self).winProb(eloA, eloB)
        expectedB = await EloComputations(self).winProb(eloB, eloA)

        eloA = await EloComputations(self).computeElo(eloA, expectedA, outcome)
        eloB = await EloComputations(self).computeElo(eloB, expectedB, 1 - outcome)
        
        async with aiosqlite.connect('elo.db') as db:
            await db.execute("UPDATE elo SET elo = ? WHERE user_id = ?", (eloA, personA.id))
            await db.execute("UPDATE elo SET elo = ? WHERE user_id = ?", (eloB, personB.id))
            
            if outcome == 1:
                await db.execute("UPDATE elo SET wins = wins + 1 WHERE user_id = ?", (personA.id,))
                await db.execute("UPDATE elo SET losses = losses + 1 WHERE user_id = ?", (personB.id,))

            else:
                await db.execute("UPDATE elo SET wins = wins + 1 WHERE user_id = ?", (personB.id,))
                await db.execute("UPDATE elo SET losses = losses + 1 WHERE user_id = ?", (personA.id,))

            await db.commit()

    async def getStats(self, user):
        async with aiosqlite.connect('elo.db') as db:
            cursor = await db.execute("SELECT wins, losses FROM elo WHERE user_id = ?", (user.id,))
            stats = await cursor.fetchone()

            if stats is None:
                await db.execute("INSERT INTO elo VALUES (?, ?, ?, ?)", (user.id, 1000, 0, 0))
                await db.commit()
                return 0, 0

            else:
                return stats[0], stats[1]  

    @commands.command()
    async def elo(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        elo = await self.getElo(member)
        
        eloEmbed = discord.Embed(color = discord.Color.blue())
        eloEmbed.set_author(name = f"{member.name}'s Elo", icon_url = member.avatar_url)
        eloEmbed.add_field(name = "Elo", value = f"{elo}")
        await ctx.send(embed = eloEmbed)

    @commands.command()
    async def compare(self, ctx, memberA: discord.Member, memberB: discord.Member = None):
        if memberB is None:
            memberB = ctx.author

        eloA = await self.getElo(memberA)
        eloB = await self.getElo(memberB)

        compareEmbed = discord.Embed(title = f"{memberB.name} vs {memberA.name}", color = discord.Color.blue())
        compareEmbed.add_field(name = "Elo", value = f"{eloA} vs {eloB}")
        compareEmbed.add_field(name = "Win Probability", value = f"{await EloComputations(self).winProb(eloA, eloB)}")
        await ctx.send(embed = compareEmbed)

    @commands.command()
    async def stats(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        wins, losses = await self.getStats(member)

        statsEmbed = discord.Embed(color = discord.Color.blue())
        statsEmbed.set_author(name = f"{member.name}'s stats", icon_url = member.avatar_url)
        statsEmbed.add_field(name = "Wins", value = wins)
        statsEmbed.add_field(name = "Losses", value = losses)

        try:
            statsEmbed.add_field(name = "Winrate", value = f"{round(wins / (wins + losses), 2) * 100}%")

        except ZeroDivisionError:
            statsEmbed.add_field(name = "Winrate", value = "0%")

        await ctx.send(embed = statsEmbed)

def setup(bot):
    bot.add_cog(Elo(bot))