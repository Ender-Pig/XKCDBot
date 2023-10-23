print("Code Started")
import discord
import feedparser
import re
from datetime import datetime,timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler

channelID = 1165750660776595630
ServerID = 1165750659715432550

Token = "MTE2NTc1MTA3MzE0Nzk5ODI4OQ.GIs_Bk.V6DHX7McUpTovv4P7His4wnpvbpnrKHtezYJR4"

try:
    with open('LastXKCD.txt','x') as f:
        f.close()
except:
    pass

def GetXKCD(Entry):
    rss = feedparser.parse('https://xkcd.com/rss.xml')
    title = rss.entries[Entry].title
    description = rss.entries[Entry].description
    link = rss.entries[Entry].link
    time = rss.entries[Entry].published
    image = re.search('src\s*=\s*"(.+?)"',description).group(1)
    number = re.search('\d+',link).group(0)
    return title,image,link,number,time 


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        await tree.sync(guild=discord.Object(id=ServerID))

        async def repeat_hourly():
            message_channel = self.get_channel(channelID)
            XKCDTitle,XKCDImage,XKCDLink,XKCDNumber,XKCDTime = GetXKCD(0)
            with open('LastXKCD.txt','r+t') as f:
                LastXKCD = f.read()
                f.close()
            if (LastXKCD != XKCDNumber) and len(LastXKCD) != 0:
                print(XKCDNumber)
                print(XKCDTitle)
                print(XKCDImage)
                print(XKCDTime)
                EmbedVar = discord.Embed(title=XKCDTitle,url=XKCDLink,color=0x8f8f8f)
                EmbedVar.set_image(url=XKCDImage)
                EmbedVar.set_footer(text=("Published "+XKCDTime[:-9]+" UTC"))
                await message_channel.send("XKCD "+XKCDNumber)
                await message_channel.send(embed=EmbedVar)
                #await message_channel.send(XKCDTitle)
                #await message_channel.send(XKCDImage)
            with open('LastXKCD.txt','w') as f:
                f.write(XKCDNumber)
                f.close()


        scheduler = AsyncIOScheduler()
        scheduler.add_job(repeat_hourly,'interval',seconds=10,start_date='2010-10-10 00:00:00')
        scheduler.start()


    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
tree = discord.app_commands.CommandTree(client)
client.run(Token)