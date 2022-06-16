from calendar import c
from socket import timeout
import sys
sys.dont_write_bytecode = True #Prevents creation of .pyc files
import random
import discord
from discord.ext import commands
import asyncio

class Connect4():
    def __init__(self):
        self.blankBoard = [["⠀:white_circle:⠀" for col in range(7)] for row in range(6)]
        self.emotes = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣"]

    class CheckWin():
        def __init__(self, board):
            self.board = board

        async def win(self, board, color):
            rows = 6
            cols = 7

            # horizontal
            for c in range(cols - 3):
                for r in range(rows):
                    if board[r][c] == color and board[r][c + 1] == color and board[r][c + 2] == color and board[r][c + 3] == color:
                        return True

            # vertical
            for c in range(cols):
                for r in range(rows - 3):
                    if board[r][c] == color and board[r + 1][c] == color and board[r + 2][c] == color and board[r + 3][c] == color:
                        return True

            # positive diagonal
            for c in range(cols - 3):
                for r in range(rows - 3):
                    if board[r][c] == color and board[r + 1][c + 1] == color and board[r + 2][c + 2] == color and board[r + 3][c + 3] == color:
                        return True

            # negative diagonal
            for c in range(cols - 3):
                for r in range(3, rows):
                    if board[r][c] == color and board[r - 1][c + 1] == color and board[r - 2][c + 2] == color and board[r - 3][c + 3] == color:
                        return True

    async def printBoard(self, board, turn = None):
        if turn == "red":
            boardEmbed = discord.Embed(title="Connect 4", description="Current turn is reflected in the embed color", color=0xD2042D)

        elif turn == "blue":
            boardEmbed = discord.Embed(title="Connect 4", description="Current turn is reflected in the embed color", color=0x4F9CC9)
        
        else:
            boardEmbed = discord.Embed(title="Connect 4", description="Current turn is reflected in the embed color", color=0xFAFAFA)

        for row in range(6):
            rowContent = ""
            for col in range(7):
                rowContent += board[row][col] + " "
            boardEmbed.add_field(name="⠀", value=rowContent, inline=False)
            
        return boardEmbed

    async def win(self, board):
        pass

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="connect4")
    async def connect4(self, ctx, opponent: discord.Member):
        #initialize game
        board = Connect4().blankBoard #current board (2d list)
        turn = random.choice(["red", "blue"]) #randomly choose who goes first
        winner = ""

        game = await Connect4.printBoard(self, board, turn) #game embed
        game.add_field(name="⠀:red_circle:", value=f"⠀{ctx.author.name}") #adds red player
        game.add_field(name=":blue_circle:", value=f"{opponent.name}") #adds blue player
        game.set_footer(text="Turn will yield after 20 seconds")
        msg = await ctx.send(embed=game)

        for emote in Connect4().emotes:
            await msg.add_reaction(f"{emote}")

        #game loop
        while True:
            #check for reactions
            if turn == "red":
                try:
                    react = await self.bot.wait_for("reaction_add", timeout=20.0, check=lambda reaction, user: user == ctx.author and str(reaction.emoji) in Connect4().emotes)

                    if str(react[0].emoji) == "1⃣":
                        row = 5
                        col = 0

                        while True:
                            if board[row][col] == "⠀:white_circle:⠀":
                                try:
                                    board[row][col] = "⠀:red_circle:⠀"

                                except IndexError:
                                    break

                                break

                            else:
                                row -= 1

                        turn = "blue"
                        await msg.clear_reactions()

                        for emote in Connect4().emotes:
                            await msg.add_reaction(f"{emote}")

                        game = await Connect4.printBoard(self, board, turn)
                        game.add_field(name="⠀:red_circle:", value=f"{ctx.author.name}") #adds red player
                        game.add_field(name=":blue_circle:", value=f"{opponent.name}") #adds blue player
                        game.set_footer(text="Turn will yield after 20 seconds")
                        await msg.edit(embed=game)

                        if await Connect4().CheckWin(board).win(board, "⠀:red_circle:⠀"):
                            winner = ctx.author
                            break

                    elif str(react[0].emoji) == "2⃣":
                        row = 5
                        col = 1

                        while True:
                            if board[row][col] == "⠀:white_circle:⠀":
                                try:
                                    board[row][col] = "⠀:red_circle:⠀"

                                except IndexError:
                                    break

                                break

                            else:
                                row -= 1

                        turn = "blue"
                        await msg.clear_reactions()

                        for emote in Connect4().emotes:
                            await msg.add_reaction(f"{emote}")

                        game = await Connect4.printBoard(self, board, turn)
                        game.add_field(name="⠀:red_circle:", value=f"{ctx.author.name}") #adds red player
                        game.add_field(name=":blue_circle:", value=f"{opponent.name}") #adds blue player
                        game.set_footer(text="Turn will yield after 20 seconds")
                        await msg.edit(embed=game)

                        if await Connect4().CheckWin(board).win(board, "⠀:red_circle:⠀"):
                            winner = ctx.author
                            break

                    elif str(react[0].emoji) == "3⃣":
                        row = 5
                        col = 2

                        while True:
                            if board[row][col] == "⠀:white_circle:⠀":
                                try:
                                    board[row][col] = "⠀:red_circle:⠀"

                                except IndexError:
                                    break

                                break

                            else:
                                row -= 1

                        turn = "blue"
                        await msg.clear_reactions()

                        for emote in Connect4().emotes:
                            await msg.add_reaction(f"{emote}")

                        game = await Connect4.printBoard(self, board, turn)
                        game.add_field(name="⠀:red_circle:", value=f"{ctx.author.name}") #adds red player
                        game.add_field(name=":blue_circle:", value=f"{opponent.name}") #adds blue player
                        game.set_footer(text="Turn will yield after 20 seconds")
                        await msg.edit(embed=game)

                        if await Connect4().CheckWin(board).win(board, "⠀:red_circle:⠀"):
                            winner = ctx.author
                            break

                    elif str(react[0].emoji) == "4⃣":
                        row = 5
                        col = 3

                        while True:
                            if board[row][col] == "⠀:white_circle:⠀":
                                try:
                                    board[row][col] = "⠀:red_circle:⠀"

                                except IndexError:
                                    break

                                break

                            else:
                                row -= 1

                        turn = "blue"
                        await msg.clear_reactions()

                        for emote in Connect4().emotes:
                            await msg.add_reaction(f"{emote}")

                        game = await Connect4.printBoard(self, board, turn)
                        game.add_field(name="⠀:red_circle:", value=f"{ctx.author.name}") #adds red player
                        game.add_field(name=":blue_circle:", value=f"{opponent.name}") #adds blue player
                        game.set_footer(text="Turn will yield after 20 seconds")
                        await msg.edit(embed=game)

                        if await Connect4().CheckWin(board).win(board, "⠀:red_circle:⠀"):
                            winner = ctx.author
                            break

                    elif str(react[0].emoji) == "5⃣":
                        row = 5
                        col = 4

                        while True:
                            if board[row][col] == "⠀:white_circle:⠀":
                                try:
                                    board[row][col] = "⠀:red_circle:⠀"

                                except IndexError:
                                    break

                                break

                            else:
                                row -= 1

                        turn = "blue"
                        await msg.clear_reactions()

                        for emote in Connect4().emotes:
                            await msg.add_reaction(f"{emote}")

                        game = await Connect4.printBoard(self, board, turn)
                        game.add_field(name="⠀:red_circle:", value=f"{ctx.author.name}") #adds red player
                        game.add_field(name=":blue_circle:", value=f"{opponent.name}") #adds blue player
                        game.set_footer(text="Turn will yield after 20 seconds")
                        await msg.edit(embed=game)

                        if await Connect4().CheckWin(board).win(board, "⠀:red_circle:⠀"):
                            winner = ctx.author
                            break

                    elif str(react[0].emoji) == "6⃣":
                        row = 5
                        col = 5
                        
                        while True:
                            if board[row][col] == "⠀:white_circle:⠀":
                                try:
                                    board[row][col] = "⠀:red_circle:⠀"

                                except IndexError:
                                    break

                                break

                            else:
                                row -= 1

                        turn = "blue"
                        await msg.clear_reactions()

                        for emote in Connect4().emotes:
                            await msg.add_reaction(f"{emote}")

                        game = await Connect4.printBoard(self, board, turn)
                        game.add_field(name="⠀:red_circle:", value=f"{ctx.author.name}") #adds red player
                        game.add_field(name=":blue_circle:", value=f"{opponent.name}") #adds blue player
                        game.set_footer(text="Turn will yield after 20 seconds")
                        await msg.edit(embed=game)

                        if await Connect4().CheckWin(board).win(board, "⠀:red_circle:⠀"):
                            winner = ctx.author
                            break

                    elif str(react[0].emoji) == "7⃣":
                        row = 5
                        col = 6
                        
                        while True:
                            if board[row][col] == "⠀:white_circle:⠀":
                                try:
                                    board[row][col] = "⠀:red_circle:⠀"

                                except IndexError:
                                    break

                                break

                            else:
                                row -= 1

                        turn = "blue"
                        await msg.clear_reactions()

                        for emote in Connect4().emotes:
                            await msg.add_reaction(f"{emote}")

                        game = await Connect4.printBoard(self, board, turn)
                        game.add_field(name="⠀:red_circle:", value=f"{ctx.author.name}") #adds red player
                        game.add_field(name=":blue_circle:", value=f"{opponent.name}") #adds blue player
                        game.set_footer(text="Turn will yield after 20 seconds")
                        await msg.edit(embed=game)

                        if await Connect4().CheckWin(board).win(board, "⠀:red_circle:⠀"):
                            winner = ctx.author
                            break

                except asyncio.TimeoutError:
                    turn = "blue"
                    await msg.clear_reactions()

                    for emote in Connect4().emotes:
                        await msg.add_reaction(f"{emote}")

                    game = await Connect4.printBoard(self, board, turn)
                    game.add_field(name="⠀:red_circle:", value=f"{ctx.author.name}") #adds red player
                    game.add_field(name=":blue_circle:", value=f"{opponent.name}") #adds blue player
                    game.set_footer(text="Turn will yield after 20 seconds")
                    await msg.edit(embed=await Connect4.printBoard(self, board, turn))
            
            #blue turn
            elif turn == "blue":
                try:
                    react = await self.bot.wait_for("reaction_add", timeout=20.0, check=lambda reaction, user: user == opponent and str(reaction.emoji) in Connect4().emotes)

                    if str(react[0].emoji) == "1⃣":
                        row = 5
                        col = 0

                        while True:
                            if board[row][col] == "⠀:white_circle:⠀":
                                try:
                                    board[row][col] = "⠀:blue_circle:⠀"

                                except IndexError:
                                    break

                                break

                            else:
                                row -= 1

                        turn = "red"
                        await msg.clear_reactions()

                        for emote in Connect4().emotes:
                            await msg.add_reaction(f"{emote}")

                        game = await Connect4.printBoard(self, board, turn)
                        game.add_field(name="⠀:red_circle:", value=f"{ctx.author.name}") #adds red player
                        game.add_field(name=":blue_circle:", value=f"{opponent.name}") #adds blue player
                        game.set_footer(text="Turn will yield after 20 seconds")
                        await msg.edit(embed=game)

                        if await Connect4().CheckWin(board).win(board, "⠀:blue_circle:⠀"):
                            winner = opponent
                            break

                    elif str(react[0].emoji) == "2⃣":
                        row = 5
                        col = 1

                        while True:
                            if board[row][col] == "⠀:white_circle:⠀":
                                try:
                                    board[row][col] = "⠀:blue_circle:⠀"

                                except IndexError:
                                    break

                                break

                            else:
                                row -= 1

                        turn = "red"
                        await msg.clear_reactions()

                        for emote in Connect4().emotes:
                            await msg.add_reaction(f"{emote}")

                        game = await Connect4.printBoard(self, board, turn)
                        game.add_field(name="⠀:red_circle:", value=f"{ctx.author.name}") #adds red player
                        game.add_field(name=":blue_circle:", value=f"{opponent.name}") #adds blue player
                        game.set_footer(text="Turn will yield after 20 seconds")
                        await msg.edit(embed=game)

                        if await Connect4().CheckWin(board).win(board, "⠀:blue_circle:⠀"):
                            winner = opponent
                            break

                    elif str(react[0].emoji) == "3⃣":
                        row = 5
                        col = 2

                        while True:
                            if board[row][col] == "⠀:white_circle:⠀":
                                try:
                                    board[row][col] = "⠀:blue_circle:⠀"

                                except IndexError:
                                    break

                                break

                            else:
                                row -= 1

                        turn = "red"
                        await msg.clear_reactions()

                        for emote in Connect4().emotes:
                            await msg.add_reaction(f"{emote}")

                        game = await Connect4.printBoard(self, board, turn)
                        game.add_field(name="⠀:red_circle:", value=f"{ctx.author.name}") #adds red player
                        game.add_field(name=":blue_circle:", value=f"{opponent.name}") #adds blue player
                        game.set_footer(text="Turn will yield after 20 seconds")
                        await msg.edit(embed=game)

                        if await Connect4().CheckWin(board).win(board, "⠀:blue_circle:⠀"):
                            winner = opponent
                            break

                    elif str(react[0].emoji) == "4⃣":
                        row = 5
                        col = 3

                        while True:
                            if board[row][col] == "⠀:white_circle:⠀":
                                try:
                                    board[row][col] = "⠀:blue_circle:⠀"

                                except IndexError:
                                    break

                                break

                            else:
                                row -= 1

                        turn = "red"
                        await msg.clear_reactions()

                        for emote in Connect4().emotes:
                            await msg.add_reaction(f"{emote}")

                        game = await Connect4.printBoard(self, board, turn)
                        game.add_field(name="⠀:red_circle:", value=f"{ctx.author.name}") #adds red player
                        game.add_field(name=":blue_circle:", value=f"{opponent.name}") #adds blue player
                        game.set_footer(text="Turn will yield after 20 seconds")
                        await msg.edit(embed=game)

                        if await Connect4().CheckWin(board).win(board, "⠀:blue_circle:⠀"):
                            winner = opponent
                            break

                    elif str(react[0].emoji) == "5⃣":
                        row = 5
                        col = 4

                        while True:
                            if board[row][col] == "⠀:white_circle:⠀":
                                try:
                                    board[row][col] = "⠀:blue_circle:⠀"

                                except IndexError:
                                    break

                                break

                            else:
                                row -= 1

                        turn = "red"
                        await msg.clear_reactions()

                        for emote in Connect4().emotes:
                            await msg.add_reaction(f"{emote}")

                        game = await Connect4.printBoard(self, board, turn)
                        game.add_field(name="⠀:red_circle:", value=f"{ctx.author.name}") #adds red player
                        game.add_field(name=":blue_circle:", value=f"{opponent.name}") #adds blue player
                        game.set_footer(text="Turn will yield after 20 seconds")
                        await msg.edit(embed=game)

                        if await Connect4().CheckWin(board).win(board, "⠀:blue_circle:⠀"):
                            winner = opponent
                            break

                    elif str(react[0].emoji) == "6⃣":
                        row = 5
                        col = 5

                        while True:
                            if board[row][col] == "⠀:white_circle:⠀":
                                try:
                                    board[row][col] = "⠀:blue_circle:⠀"

                                except IndexError:
                                    break

                                break

                            else:
                                row -= 1

                        turn = "red"
                        await msg.clear_reactions()

                        for emote in Connect4().emotes:
                            await msg.add_reaction(f"{emote}")

                        game = await Connect4.printBoard(self, board, turn)
                        game.add_field(name="⠀:red_circle:", value=f"{ctx.author.name}") #adds red player
                        game.add_field(name=":blue_circle:", value=f"{opponent.name}") #adds blue player
                        game.set_footer(text="Turn will yield after 20 seconds")
                        await msg.edit(embed=game)

                        if await Connect4().CheckWin(board).win(board, "⠀:blue_circle:⠀"):
                            winner = opponent
                            break

                    elif str(react[0].emoji) == "7⃣":
                        row = 5
                        col = 6

                        while True:
                            if board[row][col] == "⠀:white_circle:⠀":
                                try:
                                    board[row][col] = "⠀:blue_circle:⠀"

                                except IndexError:
                                    break

                                break

                            else:
                                row -= 1

                        turn = "red"
                        await msg.clear_reactions()

                        for emote in Connect4().emotes:
                            await msg.add_reaction(f"{emote}")

                        game = await Connect4.printBoard(self, board, turn)
                        game.add_field(name="⠀:red_circle:", value=f"{ctx.author.name}") #adds red player
                        game.add_field(name=":blue_circle:", value=f"{opponent.name}") #adds blue player
                        game.set_footer(text="Turn will yield after 20 seconds")
                        await msg.edit(embed=game)

                        if await Connect4().CheckWin(board).win(board, "⠀:blue_circle:⠀"):
                            winner = opponent
                            break

                except asyncio.TimeoutError:
                    turn = "red"
                    await msg.clear_reactions()

                    for emote in Connect4().emotes:
                        await msg.add_reaction(f"{emote}")

                    game = await Connect4.printBoard(self, board, turn)
                    game.add_field(name="⠀:red_circle:", value=f"{ctx.author.name}") #adds red player
                    game.add_field(name=":blue_circle:", value=f"{opponent.name}") #adds blue player
                    game.set_footer(text="Turn will yield after 20 seconds")
                    await msg.edit(embed=await Connect4.printBoard(self, board, turn))

        #end of game
        await msg.clear_reactions()
        game = await Connect4.printBoard(self, board)
        game.add_field(name="⠀:red_circle:", value=f"{ctx.author.name}") #adds red player
        game.add_field(name=":blue_circle:", value=f"{opponent.name}") #adds blue player
        game.set_footer(text="Game Over")
        await msg.edit(embed=game)
        await ctx.send(f"{winner.mention} has won!")

def setup(bot):
    bot.add_cog(Games(bot))