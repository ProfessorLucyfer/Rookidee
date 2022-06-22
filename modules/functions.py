import discord
from discord.ext import commands
from discord.ext.commands import BadArgument, Cog
from io import BytesIO
import random, emoji, re, sys
import numpy as np

class functions(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clearup(self, ctx, amount:int=0):
        await ctx.message.delete()
        await ctx.message.channel.purge(limit=amount)


    @commands.command()
    async def flip(self, ctx):
        options = ['Heads','Tails','Side']
        selection = np.random.choice(options,1,p=[0.49, 0.49, 0.02])
        await ctx.send(selection[0]) 


    @commands.command()
    async def poll(self, ctx, *, a:str):
        id = ctx.message.author.id
        emoji_init_string = str(emoji.emoji_lis(a))
        disc_emoji_sep = re.findall(r"':([^:']*):'", emoji.demojize(emoji_init_string))
        disc_emoji_string = emoji.emojize(str([''.join(':' + demoji + ':') 
                                        for demoji in disc_emoji_sep]))
        disc_emoji = re.findall(r"'([^']*)'", disc_emoji_string)
        custom_emojis = re.findall(r'<([^>]*)>', a)
        cemojilist = [''.join('<' + cemoji + '>') for cemoji in custom_emojis]
        all_emojis = disc_emoji + cemojilist
        poll = await ctx.send("**Poll from** <@" + str(id) + ">**!!**\n"
                            ""+ a)
        for i in all_emojis:
            try:
                await poll.add_reaction(i)
            except:
                print("Emoji " + i + " not found")


    @commands.command()
    async def dice(self, ctx, *,initial_input:str=""):
        listed_input = initial_input.split(" ")
        sides = 6 ; amount = 1
        for i in listed_input:
            if i.endswith("s"):
                sides = int(i.split("s")[0])
            
            if i.endswith("a"):
                amount = int(i.split("a")[0])
        
        if sides>60 or sides<1 or amount<1 or amount>10:
            await ctx.send("Maximum allowed dice is 10, maximum allowed sides on each die is 60. Numbers must be positive")
            return

        dice_throws = [] ; i = 0
        while i<amount:
            i+=1
            throw = random.sample(range(1, (sides+1)),1)
            dice_throws.append(throw)
            seed = random.randrange(sys.maxsize)
            random.Random(seed)
        dice_throws.sort()
        result = [str(i) for i in dice_throws]
        text = ", ".join(result)
        await ctx.send("**Result**\n" + f"{text}")


def setup(client):
    client.add_cog(functions(client))