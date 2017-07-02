import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup

class twoX:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def next2x(self):
        """This does stuff!"""

        #Your code will go here
        website = 'https://e8tdwagy36.execute-api.us-west-2.amazonaws.com/prod/getTimeUntilNextEvent'
        r = requests.get(website)
        soup = BeautifulSoup(r.text, 'lxml')
        for datapull in soup.find_all('body'):
            if datapull.text is None:
                await self.bot.say("The next 2x is scheduled in:" + datapull.text + ".")
            else:
                await self.bot.say("I don't think 2x is scheduled.")

def setup(bot):
    bot.add_cog(twoX(bot))
