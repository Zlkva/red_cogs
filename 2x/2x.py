import discord
from discord.ext import commands
import urllib.request
import re
import time
import datetime
from datetime import datetime, timedelta

# assumptions (if any of these are false behavior is undefined)

# news page will always have a 2x article
# event page url contains the dates of the event (ex. 12-10-12-11) which are listed in pairs
# daylight savings time does not exist (see below)
# format of times is always ##:## AM or ##:## PM
# times are always listed in pairs where the first is a start time and the second is an end time
# 2x events take place in the current year (this code won't work if it's dec 31 and there's an event on jan 1)

class twoXcog:
    """Finds the next 2x time"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def next2x(self):

        timedict = {}
        timedict['12:00AM'] = 0
        timedict['1:00AM'] = 1
        timedict['2:00AM'] = 2
        timedict['3:00AM'] = 3
        timedict['4:00AM'] = 4
        timedict['5:00AM'] = 5
        timedict['6:00AM'] = 6
        timedict['7:00AM'] = 7
        timedict['8:00AM'] = 8
        timedict['9:00AM'] = 9
        timedict['10:00AM'] = 10
        timedict['11:00AM'] = 11
        timedict['12:00PM'] = 12
        timedict['1:00PM'] = 13
        timedict['2:00PM'] = 14
        timedict['3:00PM'] = 15
        timedict['4:00PM'] = 16
        timedict['5:00PM'] = 17
        timedict['6:00PM'] = 18
        timedict['7:00PM'] = 19
        timedict['8:00PM'] = 20
        timedict['9:00PM'] = 21
        timedict['10:00PM'] = 22
        timedict['11:00PM'] = 23

        add_hours_for_testing = 0

        # will need to be changed to -7 during daylight savings
        # or look into "pytz" module for more accurate pst/pdt calculation
        pst_timedifference = -8

        currentyear = datetime.utcnow().year
        currenttimepst = datetime.utcnow() + timedelta(hours=pst_timedifference) + timedelta(hours=add_hours_for_testing)

        linkPart = []
        mainPage = ("http://maplestory.nexon.net/news")
        try:
            try:
                htmltext = urllib.request.urlopen(mainPage).read().decode('utf-8')
                regex = '<h3>[\s\S]*?<a href="/news/(\d+?)/[\w-]*?-([\d-]*)">(.*?)</a>[\s\S]*?<p>(.*?)</p>'
                matches = re.findall(re.compile(regex),htmltext)
                match = "none"

                for i in range(0, len(matches)):
                    temp = matches[i]
                    linktitle = temp[2]
                    linkdesc = temp[3]
                    if "2x" in linktitle or "2x" in linkdesc:
                        match = temp

                if match == "none":
                    match = []
                    raise Exception()
            except:
                await self.bot.say ("The next 2x event has not been announced yet in a supported format.")
            eventpageid = match[0]
            monthsanddays = re.findall(re.compile('[0-9]{1,2}'),match[1])
            
            eventPage = "http://maplestory.nexon.net/news/" + eventpageid
            try:
                htmltext = urllib.request.urlopen(eventPage).read().decode('utf-8')
                regex = '<h1.*?2x[\s\S]*?(.*?PST[\s\S]*)' #read from 2x section
                htmltext = re.findall(re.compile(regex),htmltext)[0]
                regex = '<strong>PST:(.+?)</strong>' #Gets the link with the event data
                timeList = re.findall(re.compile(regex),htmltext)
                
                startTimes = []
                endTimes = []
                
                for i in range(0, int(len(monthsanddays)/2)):
                    t = timeList[i]
                    temp = re.sub(' ', '', t)
                    newList = re.findall(re.compile("[0-9]{1,2}:[0-9]{2}[AP]M"),temp)
                
                    for j, n in enumerate(newList):
                        eventdatetime = datetime(currentyear, int(monthsanddays[0]), int(monthsanddays[1])).replace(hour=timedict[n])
                        
                        if eventdatetime - currenttimepst > timedelta(seconds=0):
                            if j % 2 == 0:
                                startTimes.append(eventdatetime)
                                #print(eventdatetime - currenttimepst)
                            else :
                                endTimes.append(eventdatetime)
                
                    monthsanddays.pop(0)
                    monthsanddays.pop(0)
                
                #print(currenttimepst, startTimes)

                if len(endTimes) == 0 and len(startTimes) == 0:
                    await self.bot.say("The next 2x event has not been announced yet.")
                
                if len(endTimes) > 0:
                    nextEndtime = endTimes[0]
                    if len(startTimes) == 0 or startTimes[0] - nextEndtime > timedelta(seconds=0):
                        timeSpan = nextEndtime.replace(microsecond=0) - currenttimepst.replace(microsecond=0)
                        await self.bot.say("The currently running 2x event ends at " + nextEndtime.strftime("%b %d %Y %H:%M:%S") + " PST (in " + str(timeSpan) + ")")
                
                if len(startTimes) > 0:
                    nextStartTime = startTimes[0]
                
                    timeSpan = nextStartTime.replace(microsecond=0) - currenttimepst.replace(microsecond=0)
                    await self.bot.say("The next 2x event starts at " + nextStartTime.strftime("%b %d %Y %H:%M:%S") + " PST (in " + str(timeSpan) + ")")
            except:
                await self.bot.say("Something broke! Try contacting @boardwalk hotel to get it fixed")
        except:
            e = 5 #Try requires an except, and except requires one line.

def setup(bot):
    bot.add_cog(twoXcog(bot))
