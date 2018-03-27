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
            for datapull in soup.findAll("h3"):

                if "2017" in datapull.text:
                    pulledtext = datapull.text
                    embed = discord.Embed(title="**No Changes Yet**", description=pulledtext, color=self.red)
                    await self.bot.say(embed=embed)
                    time.sleep(1800)

                elif "2018" in datapull.text:
                    pulledtext = datapull.text
                    sayme = "@everyone"
                    sayme += pulledtext
                    embed = discord.Embed(title=":tada: **IT'S TIME** :tada:", description=sayme, color=self.green)
                    await self.bot.say(embed=embed)
                    time.sleep(10)
                else:
                    break

def setup(bot):
    bot.add_cog(paxcheck(bot))
