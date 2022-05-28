import sys
sys.dont_write_bytecode = True #Prevents creation of .pyc files
import random
import discord
from discord.ext import commands, tasks
import aiosqlite
from rich.console import Console

console = Console() #Rich console

class Gambling(commands.Cog):
    def __init__(self):
        pass

    async def coinFlip(self):
        coin = ["heads", "tails"]
        return coin[random.randint(0, 1)]

    async def rollDice(self):
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)

        return die1 + die2

    class Blackjack():
        def __init__(self):
            self.deck = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
            self.faceCards = ["J", "Q", "K"]

        async def deal(self):
            card1 = random.choice(self.deck)
            card2 = random.choice(self.deck)

            if card1 in self.faceCards:
                card1 = "10"

            elif card1 == "A":
                card1 = "11"
            
            if card2 in self.faceCards:
                card2 = "10"

            elif card2 == "A":
                card2 = "11"

            return int(card1) + int(card2)
            
        async def hit(self):
            card = random.choice(self.deck)

            if card in self.faceCards:
                card = "10"

            elif card == "A":
                card = "11"

            return int(card)

        async def win(self, player, dealer):
            if player > dealer and (player <= 21 and dealer <= 21):
                return True

            elif player == 21 and dealer != 21:
                return True

            else:
                return False

class PvP(commands.Cog):
    def __init__(self):
        pass

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Account management
    @commands.command(name= "createacc")
    async def createAcc(self, ctx):
        async with aiosqlite.connect('database.db') as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT user_id FROM economy WHERE user_id = ?", (ctx.author.id,))
                account = await cursor.fetchone()

                if account is None:
                    await cursor.execute("INSERT INTO economy (user_id, balance, server_id) VALUES (?, ?, ?)", (ctx.author.id, 500, ctx.guild.id))
                    await ctx.send("Account created for {0.mention}!".format(ctx.author))
                    console.log("Account created for {0}!".format(ctx.author))

                else:
                    await ctx.send("You already have an account!")
                    console.log("{0} already has an account!".format(ctx.author))
                
            await db.commit()

    @commands.command(name= "deleteacc")
    async def deleteAcc(self, ctx):
        async with aiosqlite.connect('database.db') as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT user_id FROM economy WHERE user_id = ?", (ctx.author.id,))
                account = await cursor.fetchone()

                if account is not None:
                    await cursor.execute("DELETE FROM economy WHERE user_id = ?", (ctx.author.id,))
                    await ctx.send("Account deleted for {0.mention}!".format(ctx.author))
                    console.log("Account deleted for {0}!".format(ctx.author))

            await db.commit()

    @commands.command(name= "balance", aliases= ["bal"])
    async def balance(self, ctx, member: discord.Member = None):
        async with aiosqlite.connect('database.db') as db:
            async with db.cursor() as cursor:
                if member is None:
                    await cursor.execute("SELECT balance FROM economy WHERE user_id = ?", (ctx.author.id,))
                    balance = await cursor.fetchone()
                    await ctx.send("{0.mention}'s balance is {1}".format(ctx.author, balance[0]))

                else:
                    await cursor.execute("SELECT balance FROM economy WHERE user_id = ?", (member.id,))
                    balance = await cursor.fetchone()
                    await ctx.send("{0.mention}'s balance is {1}".format(member, balance[0]))

            await db.commit()

    @commands.command(name= "pay", aliases= ["give"])
    async def pay(self, ctx, member: discord.Member, amount: int):
        async with aiosqlite.connect('database.db') as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT balance FROM economy WHERE user_id = ?", (ctx.author.id,))
                balance = await cursor.fetchone()

                if balance[0] >= amount:
                    await cursor.execute("UPDATE economy SET balance = balance - ? WHERE user_id = ?", (amount, ctx.author.id))
                    await cursor.execute("UPDATE economy SET balance = balance + ? WHERE user_id = ?", (amount, member.id))
                    await ctx.send("{0} paid {1} {2}".format(ctx.author, member, amount))

                else:
                    await ctx.send("You don't have enough money to pay {0.mention} {1}".format(member, amount))

            await db.commit()

    #Casino commands
    @commands.command(name= "coinflip", aliases= ["cf"])
    async def coinFlip(self, ctx, bet: int, guess: str):
        async with aiosqlite.connect('database.db') as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT balance FROM economy WHERE user_id = ?", (ctx.author.id,))
                balance = await cursor.fetchone()

                if (balance[0] - bet) < 0:
                    await ctx.send("You don't have enough money to play!")

                else:
                    if guess.lower() == await Gambling.coinFlip(self):
                        await ctx.send("{0.mention} guessed {1} and won {2}".format(ctx.author, guess, bet * 2))      

                        await cursor.execute("SELECT balance FROM economy WHERE user_id = ?", (ctx.author.id,))
                        balance = await cursor.fetchone()
                        await cursor.execute("UPDATE economy SET balance = balance + ? WHERE user_id = ?", (bet, ctx.author.id))

                    else:
                        await ctx.send("{0.mention} guessed {1} and lost {2}".format(ctx.author, guess, bet))

                        await cursor.execute("SELECT balance FROM economy WHERE user_id = ?", (ctx.author.id,))
                        balance = await cursor.fetchone()
                        await cursor.execute("UPDATE economy SET balance = balance - ? WHERE user_id = ?", (bet, ctx.author.id))         

            await db.commit()           

    @commands.command(name= "dice")
    async def rollDice(self, ctx):
        async with aiosqlite.connect('database.db') as db:
            async with db.cursor() as cursor:
                roll = await Gambling.rollDice(self)

                if roll == 7:
                    await ctx.send("{0.mention} rolled {1} and won 100".format(ctx.author, roll))

                    await cursor.execute("SELECT balance FROM economy WHERE user_id = ?", (ctx.author.id,))
                    balance = await cursor.fetchone()
                    await cursor.execute("UPDATE economy SET balance = balance + ? WHERE user_id = ?", (100, ctx.author.id))

                else:
                    await ctx.send("You rolled a {0} you lose".format(roll))

            await db.commit()

    @commands.command(name= "blackjack")
    async def blackJack(self, ctx, bet: int):
        async with aiosqlite.connect('database.db') as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT balance FROM economy WHERE user_id = ?", (ctx.author.id,))
                balance = await cursor.fetchone()

                if (balance[0] - bet) < 0:
                    await ctx.send("You don't have enough money to play!")

                else:
                    player = await Gambling.Blackjack().deal()
                    dealer = await Gambling.Blackjack().deal()

                    embed = discord.Embed(title="Blackjack", description= "✅ To hit, ❌ to stand", color=0x00ff00)
                    embed.add_field(name="Your Hand", value=player)
                    msg = await ctx.send(embed=embed)
                    await msg.add_reaction("✅")
                    await msg.add_reaction("❌")

                while True:
                    try:
                        #checks for reaction
                        react = await self.bot.wait_for('reaction_add', timeout=10.0, check=lambda reaction, user: user == ctx.author and str(reaction.emoji) in ["✅", "❌"])

                        #hit
                        if str(react[0].emoji) == "✅":
                            await msg.clear_reactions()
                            await msg.add_reaction("✅")
                            await msg.add_reaction("❌")

                            player += await Gambling.Blackjack().hit()
                            updated_embed = discord.Embed(title="Blackjack", description= "✅ To hit, ❌ to stand", color=0x00ff00)
                            updated_embed.add_field(name="Your Hand", value=player)
                            await msg.edit(embed=updated_embed)

                            if player > 21:
                                await msg.clear_reactions()
                                updated_embed = discord.Embed(title="Blackjack", color=0x00ff00)
                                updated_embed.add_field(name="Dealer", value=dealer)
                                updated_embed.add_field(name="You", value=player)
                                await msg.edit(embed=updated_embed)

                                await ctx.send("{0.mention} lost {1}".format(ctx.author, bet))

                                await cursor.execute("SELECT balance FROM economy WHERE user_id = ?", (ctx.author.id,))
                                balance = await cursor.fetchone()
                                await cursor.execute("UPDATE economy SET balance = balance - ? WHERE user_id = ?", (bet, ctx.author.id))
                                break
                                

                        else:
                            await msg.clear_reactions()
                            updated_embed = discord.Embed(title="Blackjack", color=0x00ff00)
                            updated_embed.add_field(name="Dealer", value=dealer)
                            updated_embed.add_field(name="You", value=player)
                            await msg.edit(embed=updated_embed)
                            result = await Gambling.Blackjack().win(player, dealer)

                            if result == True:
                                await ctx.send("{0.mention} won {1}".format(ctx.author, bet * 2))

                                await cursor.execute("SELECT balance FROM economy WHERE user_id = ?", (ctx.author.id,))
                                balance = await cursor.fetchone()
                                await cursor.execute("UPDATE economy SET balance = balance + ? WHERE user_id = ?", (bet * 2, ctx.author.id))
                                break

                            else:
                                await ctx.send("{0.mention} lost {1}".format(ctx.author, bet))

                                await cursor.execute("SELECT balance FROM economy WHERE user_id = ?", (ctx.author.id,))
                                balance = await cursor.fetchone()
                                await cursor.execute("UPDATE economy SET balance = balance - ? WHERE user_id = ?", (bet, ctx.author.id))
                                break

                    except TimeoutError: 
                        msg.clear_reactions()
                        updated_embed = discord.Embed(title="Blackjack", color=0x00ff00)
                        updated_embed.add_field(name="Dealer", value=dealer)
                        updated_embed.add_field(name="You", value=player)
                        result = await Gambling.Blackjack().win(player, dealer)

                        if result == True:
                            await ctx.send("{0.mention} won {1}".format(ctx.author, bet * 2))

                            await cursor.execute("SELECT balance FROM economy WHERE user_id = ?", (ctx.author.id,))
                            balance = await cursor.fetchone()
                            await cursor.execute("UPDATE economy SET balance = balance + ? WHERE user_id = ?", (bet * 2, ctx.author.id))

                        else:
                            await ctx.send("{0.mention} lost {1}".format(ctx.author, bet))

                            await cursor.execute("SELECT balance FROM economy WHERE user_id = ?", (ctx.author.id,))
                            balance = await cursor.fetchone()
                            await cursor.execute("UPDATE economy SET balance = balance - ? WHERE user_id = ?", (bet, ctx.author.id))
                        
                        break

            await db.commit()

def setup(bot):
    bot.add_cog(Economy(bot))
    console.log("[bright_cyan]Economy Cog loaded...[/bright_cyan]")
