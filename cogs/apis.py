from pydoc import describe
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
            comic = random.randint(1, 2632)
            url = f'https://xkcd.com/{comic}/info.0.json'

            async with request('GET', url) as r:
                if r.status == 200:
                    data = await r.json()
                    comicEmbed = discord.Embed(title=data['title'], description=data['alt'], color=0xFAFAFA)
                    comicEmbed.set_image(url=data['img'])
                    comicEmbed.set_footer(text=f'Comic #{comic}')

                    await ctx.send(embed=comicEmbed)

                else:
                    await ctx.send('An error occurred.')

        elif comic.lower() == 'latest':
            url = 'https://xkcd.com/info.0.json'

            async with request('GET', url) as r:
                if r.status == 200:
                    data = await r.json()
                    comicEmbed = discord.Embed(title=data['title'], description=data['alt'], color=0xFAFAFA)
                    comicEmbed.set_image(url=data['img'])
                    comicEmbed.set_footer(text=f'Comic #{data["num"]}')

                    await ctx.send(embed=comicEmbed)
                
                else:
                    await ctx.send('An error occurred.')

        elif comic.isdigit():
            comic = int(comic)

            if comic < 1 or comic > 2632:
                await ctx.send('Comic not found.')
                return

            else:
                url = f'https://xkcd.com/{comic}/info.0.json'

                async with request('GET', url) as r:
                    if r.status == 200:
                        data = await r.json()
                        comicEmbed = discord.Embed(title=data['title'], description=data['alt'], color=0xFAFAFA)
                        comicEmbed.set_image(url=data['img'])
                        comicEmbed.set_footer(text=f'Comic #{comic}')

                        await ctx.send(embed=comicEmbed)

                    else:
                        await ctx.send('An error occurred.')

    @commands.command(name="capybara", aliases=['capy'])
    async def capybara(self, ctx, query):
        if query == 'image':
            url = 'https://api.capybara-api.xyz/v1/image/random'

            async with request('GET', url) as r:
                if r.status == 200:
                    data = await r.json()
                    capyEmbed = discord.Embed(title='Capybara Image', color=0x966841)
                    capyEmbed.set_image(url=data['image_urls']['original'])

                    await ctx.send(embed=capyEmbed)
                    
                else:
                    await ctx.send('An error occurred.')

        elif query == 'fact':
            url = 'https://api.capybara-api.xyz/v1/facts/random'

            async with request('GET', url) as r:
                if r.status == 200:
                    data = await r.json()
                    capyEmbed = discord.Embed(title='Capybara Fact', description= data['fact'], color=0x966841)

                    await ctx.send(embed=capyEmbed)
                    
                else:
                    await ctx.send('An error occurred.')

def setup(bot):
    bot.add_cog(APIs(bot))