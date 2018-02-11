import os
import inspect
import discord
from .utils import checks
from datetime import datetime
from discord.ext import commands
from .utils.dataIO import dataIO
from __main__ import user_allowed
from __main__ import send_cmd_help
from cogs.utils.dataIO import dataIO

DB_VERSION = 1

class maplemaint:

    """Finds the next 2x time"""

    def __init__(self, bot):
        self.bot = bot
        self.settings_file = 'data/maplemaint/settings.json'
        self.settings = dataIO.load_json(self.settings_file)
        self.green = discord.Color.green()
        self.orange = discord.Color.orange()
        self.red = discord.Color.red()
        self.blue = discord.Color.blue()
        
    async def _validate_server(self, server):
        return True if server.id in self.settings else False

    async def _save_settings(self):
        dataIO.save_json(self.settings_file, self.settings)

    @commands.command(pass_context=True)
    @checks.mod_or_permissions(administrator=True)
    async def add2x(self, ctx, date: str=None):

        url = "https://e2tg4byzod.execute-api.us-west-2.amazonaws.com/prod/setEventDay?date="
        combined = url + date
        headers = {'user-agent': 'Mozilla/5.0'}
        r = requests.get(combined, headers=headers)
        await self.bot.say(date + " has been added to the 2x list.");
        
    @commands.command(pass_context=True)
    @checks.mod_or_permissions(administrator=True)
    async def del2x(self, ctx, date: str=None):

        url = "https://8f9h5yxd20.execute-api.us-west-2.amazonaws.com/prod/unsetEventDay?date="
        combined = url + date
        headers = {'user-agent': 'Mozilla/5.0'}
        r = requests.get(combined, headers=headers)
        await self.bot.say(date + " has been removed to the 2x list.");


def check_folder():
    if not os.path.exists('data/maplemaint'):
        print('Creating data/maplemaint folder...')
        os.makedirs('data/maplemaint')
    if not os.path.exists('data/maplemaint/logs'):
        print('Creating data/maplemaint/logs folder...')
        os.makedirs('data/maplemaint/logs')


def check_file():
    data = {}

    data['db_version'] = DB_VERSION
    settings_file = 'data/maplemaint/settings.json'
    if not dataIO.is_valid_json(settings_file):
        print('Creating default settings.json...')
        dataIO.save_json(settings_file, data)
    else:
        check = dataIO.load_json(settings_file)
        if 'db_version' in check:
            if check['db_version'] < DB_VERSION:
                data = {}
                data['db_version'] = DB_VERSION
                print('MAPLE MAINT: Database version too old, please rerun the setup!')
                dataIO.save_json(settings_file, data)

def setup(bot):
    check_folder()
    check_file()
    cog = maplemaint(bot)
    bot.add_cog(cog)
