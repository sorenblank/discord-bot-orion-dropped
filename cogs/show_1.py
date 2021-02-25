                                ###################
                                #importing modules#
                                ###################

#importing discord modules
import discord
from discord import Intents
from discord.ext import commands
from discord.ext import commands, tasks
#importing other modules
import random
import os
import asyncio
import json
import datetime
import wikipedia as wiki
import math
import sqlite3
from PIL import Image
from io import BytesIO
import numpy as np
import re

base = sqlite3.connect("all.db")
cur = base.cursor()

class S_1(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("S1 is Loaded ----")

    @commands.group(invoke_without_command = True,case_insensitive=True)
    async def show(self,ctx):
        show_embed = discord.Embed(title='= = = = = = = =| Help - [Show] |= = = = = = = =',description= "-------------------------------------------------------------")
        show_embed.set_author(name='Show Commands',icon_url=f'{self.client.user.avatar_url}')




        show_embed.set_footer(icon_url=ctx.author.avatar_url,text=f"Requested by {ctx.author.name}")
        await ctx.send(embed = show_embed)

    #This part sends the list of channels that are set as announcement channel 
    @show.command(aliases = ['announcement','announce'])
    async def announcements(self,ctx,msg):
        if msg.lower() == 'channels' or msg.lower() == 'channel':
            cur.execute("SELECT*FROM Announce_ch")
            all = cur.fetchall()
            an_guilds = []
            for i in all:
                an_guilds.append(i[0])
            
            if ctx.guild.id in an_guilds:
                cur.execute("SELECT*FROM Announce_ch WHERE Guild Like ?",(ctx.guild.id,))
                all = cur.fetchall()

                channels = ""
                num = 1
                for i in all:
                    channels = channels + f"0{num}| <#{i[1]}>\n "
                    num = num + 1

                if len(all) != 0:
                    embed = discord.Embed(title = "= = = = =| All Announcement Channels |= = = = =")
                    embed.set_author(name='Announcement Channels',icon_url=f'{self.client.user.avatar_url}')
                    embed.add_field(name = "------------------ 📃 __Channels__ 📃 -------------------",value = channels, inline= True)
                    embed.set_footer(icon_url=ctx.author.avatar_url, text= f"Requested by {ctx.author.name}")
                    await ctx.send(embed = embed)
                    
            if ctx.guild.id not in an_guilds:
                await ctx.send("This server has no announcement channel set for me.")
            


def setup(client):
    client.add_cog(S_1(client))