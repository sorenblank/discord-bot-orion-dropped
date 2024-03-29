import discord
from discord import Intents
from discord.ext import commands
from discord.ext import commands, tasks
import random
import asyncio
import math
from PIL import Image
from io import BytesIO
import numpy as np
import re
import os
import asyncio
import pymongo
from pymongo import MongoClient


cluster = MongoClient("mongodb+srv://soren:cdD2_qWUYRk-d4G@orion.iztml.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
base = cluster["OrionDB"]
tc_cur = base["tc"]
class Tic(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Tic is Loaded ----")

    @commands.command(aliases = ["tictactoe","tic"])
    async def tictac(self, ctx, member:discord.Member=None):
        raw = tc_cur.find({})
        guilds = []
        channels = []
        try:
            x = [i for i in raw]
            guilds = [x[i]["guild"] for i in range(len(x))]
            channels = [x[i]["channel"] for i in range(len(x))]
        except:
            pass
        

        if ctx.guild.id in guilds:
            if ctx.channel.id in channels:
                if member==None:
                    await ctx.send("You can\'t play alone bruh.")
                elif member==ctx.author:
                    await ctx.send("Are you serious?")
                elif member.bot:
                    await ctx.send("Come on! Go find a human to play tic-tac-toe with.")
                else:
                    await ctx.send(f"{member.mention}, you are being challenged on a game of tic-tac-toe by {ctx.author.mention}")
                    msg=await ctx.send("If you accept the challenge, respond by clicking on the ✅ reaction. If you wanna decline the challenge click on the ❎ reaction. Do it, within a minute!")
                    reactions = ["✅", "❎"]
                    for r in reactions:
                        await msg.add_reaction(r)

                    def check(reaction, user):
                        return user == member and str(reaction.emoji) in reactions
                    try:
                        reaction, user = await self.client.wait_for('reaction_add', timeout=60, check=check)
                        if str(reaction.emoji)=="❎":
                            await ctx.send(f"{ctx.author.mention}, {member.mention} declined your challenge.")
                        else:
                            await ctx.send(file=discord.File('./TicTac/Board_example.png'))
                            await ctx.send(f"{ctx.author.mention} {member.mention} Memorize these board positions.")
                            mes=await ctx.send(f"{member.mention} react on this message, which one you wanna take: :x: or :o:")
                            xoxo=["❌","⭕"]
                            for xo in xoxo:
                                await mes.add_reaction(xo)
                            def chec(reaction,user):
                                return user == member and str(reaction.emoji) in xoxo
                            reac, user = await self.client.wait_for('reaction_add', check=chec)
                            await ctx.send("Now we\'ll have a coin toss, whoever wins the toss gets to start first.")
                            w=random.choice(xoxo)
                            await ctx.send(w)
                            xoxo.remove(w)
                            if w==str(reac.emoji):
                                F=member
                                L=ctx.author
                                dict={member:w,ctx.author:xoxo[0]}
                            else:
                                F=ctx.author
                                L=member
                                dict={ctx.author:w,member:xoxo[0]}
                            
                            def tt(member):
                                if dict.get(member)=="❌":
                                    return 'tic'
                                elif dict.get(member)=="⭕":
                                    return 'tac'
                            
                            await ctx.send(f"Congratulations {F.mention}! You\'re gonna start first.")
                            game_ongoing=True
                            move=F
                            AA=np.zeros((3,3))
                            
                            template=Image.open('./TicTac/Board.png')
                            tic=Image.open('./TicTac/X.png')
                            tac=Image.open('./TicTac/O.png')
                            
                            sq00=(3,6)
                            sq01=(214,9)
                            sq02=(420,9)
                            sq10=(7,213)
                            sq11=(213,214)
                            sq12=(419,213)
                            sq20=(7,421)
                            sq21=(213,420)
                            sq22=(419,420)
                            sq=np.empty((3,3),object)
                            sq[0][0]=sq00
                            sq[0][1]=sq01
                            sq[0][2]=sq02
                            sq[1][0]=sq10
                            sq[1][1]=sq11
                            sq[1][2]=sq12
                            sq[2][0]=sq20
                            sq[2][1]=sq21
                            sq[2][2]=sq22

                            while game_ongoing==True:
                                await ctx.send(f"{move.mention} It\'s your turn. If you wanna place at the (x,y)-th cell, just send `(x,y)`")
                                def chk(author):
                                    def inner_check(message):
                                        B1=len(message.content)==5
                                        B2=message.content[0]=="("
                                        B3=message.content[-1]==")"
                                        B4=bool(re.search(r'\d', message.content))
                                        B5="," in message.content
                                        B6=message.author == author
                                        B7= message.channel==ctx.channel
                                        return B1 and B2 and B3 and B4 and B5 and B6 and B7
                                    return inner_check

                                mm=await self.client.wait_for('message', check=chk(move))
                                mmm=mm.content.replace('(','')
                                mmm=mmm.replace(')','')
                                sp=mmm.split(',')
                                x=int(sp[0])
                                y=int(sp[1])
                                while x not in range(3) or y not in range(3):
                                    await ctx.send("Did you not memorize the positions?")
                                    mm=await self.client.wait_for('message', check=chk(move))
                                    mmm=mm.content.replace('(','')
                                    mmm=mmm.replace(')','')
                                    sp=mmm.split(',')
                                    x=int(sp[0])
                                    y=int(sp[1])
                                
                                while AA[x][y] != 0:
                                    await ctx.send("Overlapping not allowed.")
                                    mm= await self.client.wait_for('message', check=chk(move))
                                    mmm=mm.content.replace('(','')
                                    mmm=mmm.replace(')','')
                                    sp=mmm.split(',')
                                    x=int(sp[0])
                                    y=int(sp[1])
                                
                                def num(move):
                                    if move==F:
                                        return 1
                                    elif move==L:
                                        return 2
                                
                                AA[x][y]=num(move)

                                if tt(move)=='tic':
                                    template.paste(tic,sq[x][y])
                                    template.save('qwerty.png')
                                    await ctx.send(file=discord.File("qwerty.png"))
                                    os.remove('qwerty.png')

                                elif tt(move)=='tac':
                                    template.paste(tac,sq[x][y])
                                    template.save('qwerty.png')
                                    await ctx.send(file=discord.File("qwerty.png"))
                                    os.remove('qwerty.png')

                                if np.count_nonzero(AA)>=5:
                                    n=num(move)
                                    C1= [n,n,n] in AA.tolist()
                                    C2= [n,n,n] in np.transpose(AA).tolist()
                                    S1= AA[0][0]==n
                                    S2= AA[1][1]==n
                                    S3= AA[2][2]==n
                                    C3= S1 and S2 and S3
                                    S4= AA[0][2]==n
                                    S5= AA[2][0]==n
                                    C4= S4 and S5 and S2
                                    
                                    if C1 or C2 or C3 or C4:
                                        player1 = 0
                                        player2 = 0

                                        if move.id == ctx.author.id:
                                            player1 = ctx.author.id
                                            player2 = member.id
                                        else:
                                            player1 = member.id
                                            player2 = ctx.author.id
                                        
                                        
                                        await ctx.send(f"Yay!! {move.mention} has won.")
                                        break

                                if move==F:
                                    move=L
                                elif move==L:
                                    move=F
                                
                                if np.count_nonzero(AA)==9:
                                    game_ongoing=False

                                    await ctx.send("The game ended up as a draw.")
                            
                    except asyncio.TimeoutError:
                        await msg.clear_reactions()
                        await ctx.send(f"{member.mention} You took a long time to respond. The challenge is dismissed.")
                        return
            
            elif ctx.channel.id not in channels:
                raw = tc_cur.find_one({"guild":ctx.guild.id})
                ch = raw["channel"]
                ch = self.client.get_channel(ch)
                await ctx.send(f"Please use this {ch.mention} channel.")

        elif ctx.guild.id not in guilds:
            await ctx.send("No channel of this server is set as **TicTacToe Channel**.\nPlease set one using this command `.o set TicTacToe (channel)`")

def setup(client):
    client.add_cog(Tic(client))