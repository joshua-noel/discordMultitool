import sys
sys.dont_write_bytecode = True #Prevents creation of .pyc files
import random
import discord
from discord.ext import commands, tasks
import aiosqlite
import asyncio
from rich.console import Console

console = Console() #Rich console

#--------------------------Emdeds--------------------------#

class Gambling(commands.Cog):
    def __init__(self):
        pass

    async def coinFlip(self):
        heads = ["heads", "head", "h"]
        tails = ["tails", "tail", "t"]
        face = random.choice(heads + tails)

        return str(face)

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
                card1 = "1"
            
            if card2 in self.faceCards:
                card2 = "10"

            elif card2 == "A":
                card2 = "1"

            return int(card1) + int(card2)
            
        async def hit(self):
            card = random.choice(self.deck)

            if card in self.faceCards:
                card = "10"

            elif card == "A":
                card = "1"

            return int(card)

        async def win(self, player, dealer):
            if player > dealer and player <= 21:
                return True

            if player < dealer and dealer > 21:
                return True

            if player == 21 and dealer != 21:
                return True

            else:
                return False

    class Roulette():
        def __init__(self):
            self.wheel = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "00"]
            self.bets = ["red", "black", "green", "even", "odd", "low", "high", "basket"]

            self.betNumbers = {
                "red": ["1", "3", "5", "7", "9", "12", "14", "16", "18", "19", "21", "23", "25", "27", "30", "32", "34", "36"],
                "black": ["2", "4", "6", "8", "10", "11", "13", "15", "17", "20", "22", "24", "26", "28", "29", "31", "33", "35"],
                "green": ["0", "00"],
                "low": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18"],
                "high": ["19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36"],
                "basket": ["0", "00", "1", "2", "3"]
            }

            self.payouts = {
                "red": 2,
                "black": 2,
                "green": 35,
                "even": 2,
                "odd": 2,
                "low": 2,
                "high": 2,
                "basket": 7
            }

        async def spin(self):
            return random.choice(self.wheel)

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
                    await cursor.execute("INSERT INTO economy (user_id, server_id, balance) VALUES (?, ?, ?)", (ctx.author.id, ctx.guild.id, 500))
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

    @commands.command(name= "beg")
    async def beg(self, ctx):
        if await self.balance(ctx) == 0:
            coins = random.randint(100, 500)
            await self.updateBalance(ctx.author, coins)
            await ctx.send("{0.mention} begged for ${1}!".format(ctx.author, coins))

        else:
            await ctx.send("You can't beg when you have money!")

    #Money handling
    async def updateBalance(self, user, amount):
        async with aiosqlite.connect('database.db') as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT balance FROM economy WHERE user_id = ?", (user.id,))
                balance = await cursor.fetchone()

                if balance is not None:
                    await cursor.execute("UPDATE economy SET balance = ? WHERE user_id = ?", (int(balance[0]) + int(amount), user.id))
                    await db.commit()

    async def balance(self, ctx, member: discord.Member = None):
        async with aiosqlite.connect('database.db') as db:
            async with db.cursor() as cursor:
                if member is None:
                    await cursor.execute("SELECT balance FROM economy WHERE user_id = ?", (ctx.author.id,))
                    balance = await cursor.fetchone()

                else:
                    await cursor.execute("SELECT balance FROM economy WHERE user_id = ?", (member.id,))
                    balance = await cursor.fetchone()

            await db.commit()
            return int(balance[0])

    @commands.command(name= "balance", aliases= ["bal"])
    async def _balance(self, ctx, member: discord.Member = None):
        if member is None:
            try:
                balance = await self.balance(ctx)

            except TypeError:
                await ctx.send("You do not have an account! I'll make one for you!")
                await self.createAcc(ctx)

            finally:
                balance = await self.balance(ctx)
                await ctx.send("{0.mention}'s balance is ${1}".format(ctx.author, balance))

        else:
            try:
                balance = await self.balance(ctx, member)

            except TypeError:
                await ctx.send("That user does not have an account! I'll make one for them!")
                await self.createAcc(ctx, member)

            finally:
                balance = await self.balance(ctx, member)
                await ctx.send("{0.mention}'s balance is ${1}".format(member, balance))

    @commands.command(name= "pay", aliases= ["give"])
    async def pay(self, ctx, member: discord.Member, amount: int):
        balance = await self.balance(ctx, ctx.author)

        if balance >= amount:
            await self.updateBalance(ctx.author, -amount)
            await self.updateBalance(member, amount)
            await ctx.send("{0} has paid {1} ${2}".format(ctx.author, member, amount))

    #Casino commands
    @commands.command(name= "coinflip", aliases= ["cf"])
    async def coinFlip(self, ctx, bet: int, guess: str):
        balance = await self.balance(ctx, ctx.author)

        if balance >= bet:
            await self.updateBalance(ctx.author, -bet)
            face = await Gambling.coinFlip(self)
            guess = guess.lower()

            if (guess in face):
                await self.updateBalance(ctx.author, bet * 2)
                await ctx.send("{0.mention} won ${1}!".format(ctx.author, bet * 2))

            else:
                await ctx.send("{0.mention} lost ${1}!".format(ctx.author, bet))

        else:
            await ctx.send("You don't have enough money!")       

    @commands.command(name= "dice")
    async def rollDice(self, ctx):
        roll = await Gambling.rollDice(self)

        if roll == 7:
            await ctx.send("{0.mention} rolled {1} and won $100".format(ctx.author, roll))
            await self.updateBalance(ctx.author, 100)

        else:
            await ctx.send("You rolled a {0} you lose".format(roll))

    @commands.command(name= "blackjack")
    async def blackJack(self, ctx, bet: int):
        balance = await self.balance(ctx, ctx.author)

        if balance < bet:
            await ctx.send("You don't have enough money to play!")

        else:
            await self.updateBalance(ctx.author, -bet)
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
                    react = await self.bot.wait_for('reaction_add', timeout=20.0, check=lambda reaction, user: user == ctx.author and str(reaction.emoji) in ["✅", "❌"])

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
                            await ctx.send("{0.mention} lost ${1}".format(ctx.author, bet))
                            break
                                
                    else:
                        while dealer < 17:
                            dealer += await Gambling.Blackjack().hit()

                        await msg.clear_reactions()
                        updated_embed = discord.Embed(title="Blackjack", color=0x00ff00)
                        updated_embed.add_field(name="Dealer", value=dealer)
                        updated_embed.add_field(name="You", value=player)
                        await msg.edit(embed=updated_embed)
                        result = await Gambling.Blackjack().win(player, dealer)

                        if player == dealer:
                            await ctx.send("{0.mention} tied with the dealer! No money lost!".format(ctx.author))
                            await self.updateBalance(ctx.author, bet)
                            break

                        if result == True:
                            await ctx.send("{0.mention} won ${1}".format(ctx.author, bet * 2.5))
                            await self.updateBalance(ctx.author, bet * 2.5)
                            break

                        else:
                            await ctx.send("{0.mention} lost ${1}".format(ctx.author, bet))
                            break

                except asyncio.TimeoutError:
                    while dealer < 17:
                        dealer += await Gambling.Blackjack().hit()

                    await msg.clear_reactions()
                    updated_embed = discord.Embed(title="Blackjack", color=0x00ff00)
                    updated_embed.add_field(name="Dealer", value=dealer)
                    updated_embed.add_field(name="You", value=player)
                    await msg.edit(embed=updated_embed)
                    result = await Gambling.Blackjack().win(player, dealer)

                    if player == dealer:
                        await ctx.send("{0.mention} tied with the dealer! No money lost!".format(ctx.author))
                        await self.updateBalance(ctx.author, bet)
                        break

                    if result == True:
                        await ctx.send("{0.mention} won ${1}".format(ctx.author, bet * 2.5))
                        await self.updateBalance(ctx.author, bet * 2.5)
                        break

                    else:
                        await ctx.send("{0.mention} lost {1}".format(ctx.author, bet))
                        break

    @commands.command(name= "roulette")
    async def roulette(self, ctx, bet: int, guess: str):
        balance = await self.balance(ctx, ctx.author)

        if balance < bet:
            await ctx.send("You don't have enough money to play!")

        else:
            await self.updateBalance(ctx.author, -bet)
            guess = guess.lower()

            if guess in Gambling.Roulette().payouts:
                payout = Gambling.Roulette().payouts[guess]
            
            else:
                await ctx.send("You didn't enter a valid guess!")
                return

            roll = await Gambling.Roulette().spin()

            if guess in Gambling.Roulette().betNumbers:
                if roll in Gambling.Roulette().betNumbers[guess]:
                    await self.updateBalance(ctx.author, bet * payout)
                    await ctx.send("Wheel landed on {0}! {1.mention} won ${2}!".format(roll, ctx.author, bet * payout))

                else:
                    await ctx.send("Wheel landed on {0}! {1.mention} lost ${2}!".format(roll, ctx.author, bet))

            elif guess == "even":
                if int(roll) % 2 == 0:
                    await self.updateBalance(ctx.author, bet * payout)
                    await ctx.send("Wheel landed on {0}! {1.mention} won ${2}!".format(roll, ctx.author, bet * payout))

                else:
                    await ctx.send("Wheel landed on {0}! {1.mention} lost ${2}!".format(roll, ctx.author, bet))

            elif guess == "odd":
                if int(roll) % 2 == 1:
                    await self.updateBalance(ctx.author, bet * payout)
                    await ctx.send("Wheel landed on {0}! {1.mention} won ${2}!".format(roll, ctx.author, bet * payout))

                else:
                    await ctx.send("Wheel landed on {0}! {1.mention} lost ${2}!".format(roll, ctx.author, bet))

def setup(bot):
    bot.add_cog(Economy(bot))