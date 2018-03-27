import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import re
import time

class paxcheck:
    """Checks paxsite.como for West date changes"""

    def __init__(self, bot):
            self.bot = bot
            self.green = discord.Color.green()
            self.orange = discord.Color.orange()
            self.red = discord.Color.red()
            self.blue = discord.Color.blue()

    @commands.command()
    async def pax(self):

        while True:
            website = 'http://www.paxsite.com/'
            r = requests.get(website)
            soup = BeautifulSoup(r.content, 'html.parser')
            soup2 = BeautifulSoup(r.content, 'html.parser')
            for datapull in soup.findAll("li", {"id": "west"}):

                if "2018" in datapull.text:
                    pulledtext = datapull.text
                    splitpull = pulledtext.splitlines()
                    firstpull = splitpull[6]
                    embed = discord.Embed(title="**No Changes Yet**", description=firstpull, color=self.red)
                    await self.bot.say(embed=embed)
                    time.sleep(10)

                elif "2017" in datapull.text:
                    pulledtext = datapull.text
                    splitpull = pulledtext.splitlines()
                    firstpull = splitpull[6]
                    sayme = "@everyone "
                    sayme += firstpull
                    embed = discord.Embed(title=":tada: **IT'S TIME** :tada:", description=sayme, color=self.green)
                    await self.bot.say(embed=embed)
                    time.sleep(10)
                else:
                    break

def setup(bot):
    bot.add_cog(paxcheck(bot))
