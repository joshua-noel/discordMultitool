import sys
sys.dont_write_bytecode = True #Prevents creation of .pyc files
import discord
from discord.ext import commands, tasks
import aiosqlite

#TODO - Update roles based on level

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.expReqDict = {
            1: 100,
            2: 300,
            3: 500,
            4: 1000,
            5: 2000,
            6: 3000,
            7: 4000,
            8: 5000,
            9: 6000,
            10: 10000
        }

    async def updateExp(self, user_id, amt):
        async with aiosqlite.connect('levels.db') as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT * FROM levels WHERE user_id = ?", (user_id,))
                data = await cursor.fetchone()

                if data is None:
                    await cursor.execute("INSERT INTO levels (user_id, exp, level) VALUES (?, ?, ?)", (user_id, 0, 1))
                    await db.commit()

                else:
                    exp = data[1] + amt
                    level = data[2]

                    if exp > self.expReqDict[level]:
                        await cursor.execute("UPDATE levels SET exp = ?, level = ? WHERE user_id = ?", (exp, level + 1, user_id))
                        await db.commit()
                        return True

                    else :
                        await cursor.execute("UPDATE levels SET exp = ? WHERE user_id = ?", (exp, user_id))
                        await db.commit()
                        return False

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.updateExp(member.id, 0)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.content.startswith(self.bot.command_prefix):
            return

        leveledUp = await self.updateExp(message.author.id, 15)

        if leveledUp:
            await message.channel.send(f"{message.author.mention} has leveled up!")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return

        levelUp = await self.updateExp(payload.member.id, 2)

        if levelUp:
            await self.bot.get_channel(payload.channel_id).send(f"{payload.member.mention} has leveled up!")

    @commands.command()
    async def level(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        async with aiosqlite.connect('levels.db') as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT * FROM levels WHERE user_id = ?", (user.id,))
                data = await cursor.fetchone()

                if data is None:
                    await cursor.execute("INSERT INTO levels (user_id, exp, level) VALUES (?, ?, ?)", (user.id, 0, 1))
                    await db.commit()
                    await ctx.send(f"{user.mention} is level 1!")

                else:
                    await ctx.send(f"{user.mention} is level {data[2]} with {data[1]} exp!")

def setup(bot):
    bot.add_cog(Leveling(bot))
        