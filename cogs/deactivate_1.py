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
from PIL import Image
from io import BytesIO
import numpy as np
import re
import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://soren:cdD2_qWUYRk-d4G@orion.iztml.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
base = cluster["OrionDB"]

fc_cur = base["fc"] #Formation = [Guild, Channel, Past_Number, Last_Number, Author]
c_cur = base["c"] #Formation = [Guild, Channel, Past_Number, Last_Number, Author]
tc_cur = base["tc"]
bc_cur = base["bc"]
ta_cur = base["ta"]
weclome_cur = base["welcome"] 
bye_cur = base["bye"] 
banner_cur = base["banner"]

class D_1(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        ("D1 is Loaded ----")

                                        ###########################
                                        ##      DEACTIVATOR      ##
                                        ###########################

    @commands.group(aliases = ["stop","eliminate","remove"],invoke_without_command = True,case_insensitive = True)
    async def deactivate(self,ctx):
        return

    @deactivate.command(aliases = ["fibo"])
    async def Fibonacci(self,ctx):
        raw = fc_cur.find({"guild":ctx.guild.id})
        guilds = []
        try:
            x = [i for i in raw]
            guilds = [x[i]["guild"] for i in range(len(x))]
        except:
            pass
        if ctx.author.guild_permissions.manage_channels:

            if ctx.guild.id in guilds:
                cooked = fc_cur.find_one({"guild":ctx.guild.id})
                ch = self.client.get_channel(cooked["channel"])
                fc_cur.delete_one({"guild":ctx.guild.id})
                await ctx.send(f"{ch.mention} is no longer a **Fibonacci** channel.")
            else:
                await ctx.send("No channel is set as **Fibonacci** channel.")

        else:
            await ctx.send("**Access Denied!**\nThis command requires `manage_channel` permission in order to execute.")

            
    @deactivate.command(aliases = ["count"])
    async def countup(self,ctx):
        raw = c_cur.find({"guild":ctx.guild.id})
        guilds = []
        try:
            x = [i for i in raw]
            guilds = [x[i]["guild"] for i in range(len(x))]
        except:
            pass
        if ctx.author.guild_permissions.manage_channels:

            if ctx.guild.id in guilds:
                cooked = c_cur.find_one({"guild":ctx.guild.id})
                ch = self.client.get_channel(cooked["channel"])
                c_cur.delete_one({"guild":ctx.guild.id})
                await ctx.send(f"{ch.mention} is no longer a **Fibonacci** channel.")
            else:
                embed = discord.Embed(color = 0x5865F2,description = "`fibonacci channel` not found.")
                embed.set_author(name = "Index ERROR", icon_url= self.client.user.avatar_url)
                await ctx.send(embed = embed)

        else:
            embed = discord.Embed(color = 0x5865F2, description = f"This command requires `manage_channel` permission in order to execute.")
            embed.set_author(name = "Access Denied", icon_url = self.client.user.avatar_url)
            await ctx.send(embed = embed)

    # @deactivate.command(aliases = ["tictactoe","tac"])
    # async def Tic(self,ctx):
    #     raw = tc_cur.find({})
    #     guilds = []
    #     channels = []
    #     try:
    #         x = [i for i in raw]
    #         guilds = [x[i]["guild"] for i in range(len(x))]
    #         channels = [x[i]["channel"] for i in range(len(x))]
    #     except:
    #         pass

    #     if ctx.author.guild_permissions.manage_channels:
    #         if ctx.guild.id in guilds:
    #             cooked = tc_cur.find_one({"guild":ctx.guild.id})
    #             ch = self.client.get_channel(cooked["channel"])
    #             tc_cur.delete_one({"guild":ctx.guild.id})
    #             await ctx.send(f"{ch.mention} is no longer a **TicTacToe** channel.")
    #         else:
    #             await ctx.send("No channel is set as **TicTacToe** channel.")
    #     else:
    #         await ctx.send("**Access Denied!**\nThis command requires `manage_channel` permission in order to execute.")


    # @deactivate.command()
    # async def battleship(self,ctx):
    #     raw = bc_cur.find({})
    #     guilds = []
    #     channels = []
    #     try:
    #         x = [i for i in raw]
    #         guilds = [x[i]["guild"] for i in range(len(x))]
    #         channels = [x[i]["channel"] for i in range(len(x))]
    #     except:
    #         pass

    #     if ctx.author.guild_permissions.manage_channels:
    #         if ctx.guild.id in guilds:
    #             cooked = bc_cur.find_one({"guild":ctx.guild.id})
    #             ch = self.client.get_channel(cooked["channel"])
    #             bc_cur.delete_one({"guild":ctx.guild.id})
    #             await ctx.send(f"{ch.mention} is no longer a **Battleship** channel.")
    #         else:
    #             await ctx.send("No channel is set as **Battleship** channel.")
    #     else:
    #         await ctx.send("**Access Denied!**This command requires `manage_channel` permission in order to execute.")

    @deactivate.command()
    async def WElcome(self,ctx):
        raw = weclome_cur.find({})
        guilds = []
        try:
            x = [i for i in raw]
            guilds = [x[i]["guild"] for i in range(len(x))]
        except:
            pass

        cooked = weclome_cur.find_one({"guild":ctx.guild.id})
        ch = self.client.get_channel(cooked["channel"])
        if ctx.author.guild_permissions.manage_guild:
            if ctx.guild.id in guilds:
                weclome_cur.delete_one({"guild":ctx.guild.id})
                await ctx.send(f"{ch.mention} is no longer a **WELCOME** channel.")
            else:
                embed = discord.Embed(color = 0x5865F2,description = "`welcome channel` not found.")
                embed.set_author(name = "Index ERROR", icon_url= self.client.user.avatar_url)
                await ctx.send(embed = embed)
        else:
            embed = discord.Embed(color = 0x5865F2, description = f"This command requires `manage_channel` permission in order to execute.")
            embed.set_author(name = "Access Denied", icon_url = self.client.user.avatar_url)
            await ctx.send(embed = embed)

    @deactivate.command()
    async def BYe(self,ctx):
        raw = bye_cur.find({})
        guilds = []
        try:
            x = [i for i in raw]
            guilds = [x[i]["guild"] for i in range(len(x))]
        except:
            pass

        cooked = bye_cur.find_one({"guild":ctx.guild.id})
        ch = self.client.get_channel(cooked["channel"])
        if ctx.author.guild_permissions.manage_guild or ctx.author.guild_permissions.administrator:
            if ctx.guild.id in guilds:
                bye_cur.delete_one({"guild":ctx.guild.id})
                await ctx.send(f"{ch.mention} is no longer a **BYE** channel.")
            else:
                await ctx.send("No channel is set as **BYE** channel.")
        else:
            await ctx.send("**Access Denied!**This command requires `manage_guilds` permission in order to execute.")
    
    @deactivate.command()
    async def banner(self,ctx):
        raw = banner_cur.find({})
        guilds = []
        try:
            x = [i for i in raw]
            guilds = [x[i]["guild"] for i in range(len(x))]
        except:
            pass

        if ctx.author.guild_permissions.manage_guild or ctx.author.guild_permissions.administrator:
            if ctx.guild.id in guilds:
                banner_cur.delete_one({"guild":ctx.guild.id})
                embed = discord.Embed(color = 0x5865F2, description = "`welcome banner` has been removed.")
                embed.set_author(name = "Deactivate Successful!", icon_url = self.client.user.avatar_url)
                await ctx.send(embed = embed)
                return
            else:
                embed = discord.Embed(color = 0x5865F2,description = "`welcome banner` not found.")
                embed.set_author(name = "Index ERROR", icon_url= self.client.user.avatar_url)
                await ctx.send(embed = embed)
                return

def setup(client):
    client.add_cog(D_1(client))