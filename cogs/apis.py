import sys
from webbrowser import get
sys.dont_write_bytecode = True #Prevents creation of .pyc files
import random
import discord
from discord.ext import commands
from aiohttp import request

class APIs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='xkcd', aliases=['xk'])
    async def xkcd(self, ctx, comic: str = None):
        """
        Get the latest xkcd comic or a specific comic.
        """
        if comic is None:
            comic = random.randint(1, 1700)
            url = f'https://xkcd.com/{comic}/info.0.json'

            async with request('GET', url) as r:
                data = await r.json()

            comicEmbed = discord.Embed(title=data['title'], description=data['alt'], color=0x00ff00)
            comicEmbed.set_image(url=data['img'])
            comicEmbed.set_footer(text=f'Comic #{comic}')
            await ctx.send(embed=comicEmbed)
        
        elif comic.lower() == 'latest':
            url = 'https://xkcd.com/info.0.json'

            async with request('GET', url) as r:
                data = await r.json()

            comicEmbed = discord.Embed(title=data['title'], description=data['alt'], color=0x00ff00)
            comicEmbed.set_image(url=data['img'])
            comicEmbed.set_footer(text=f'Comic #{data["num"]}')
            await ctx.send(embed=comicEmbed)

        elif comic.isdigit():
            comic = int(comic)

            if comic < 1 or comic > 1700:
                await ctx.send('Comic not found.')
                return

            else:
                url = f'https://xkcd.com/{comic}/info.0.json'

                async with request('GET', url) as r:
                    data = await r.json()

                comicEmbed = discord.Embed(title=data['title'], description=data['alt'], color=0x00ff00)
                comicEmbed.set_image(url=data['img'])
                comicEmbed.set_footer(text=f'Comic #{comic}')
                await ctx.send(embed=comicEmbed)

def setup(bot):
    bot.add_cog(APIs(bot))