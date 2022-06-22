import discord, asyncio
from discord.ext import commands
import random, json

class feeding(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.feedMax = random.randint(10, 100) # When bot starts, the initial max limit is set (random number between a and b (10, 100))
        self.feedCurrent = 0
        self.isOverfed = False
    
    async def sendFeedEmbed(self, ctx):
        embed = discord.Embed(
        colour = discord.Colour.green())
        embed.add_field(
            name='Rookidee is enjoying the food',
            value=f"{ctx.author.mention} fed Rookidee! <:rookieat:989291327009202196> \n Rookidee has been fed {self.feedCurrent}x times!"
            )
        await ctx.send(embed=embed)

    async def sendFoodComaEmbed(self, ctx):
        embed = discord.Embed(
        colour = discord.Colour.red())
        embed.add_field(
            name='*Rookidee is in food coma!*',
            value=f"Rookidee ate {self.feedCurrent}x times and is now sleeping. <:rookisleep:989291356033785909> \n Please try feeding him again later!")       
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def feedReset(self, ctx):
        self.feedMax = random.randint(10, 100) # Same as when bot starts
        self.feedCurrent = 0
        self.isOverfed = False


    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def feedCheckMax(self, ctx):
        with open("data/settings.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
            guild_dict = data[str(ctx.message.guild.id)]
        prefix = guild_dict["prefix"]
        await ctx.send(
            f"Current feed limit is {self.feedMax}\nYou can set a new limit with `{prefix}feedSetMax [number]`"+
            "\nIf you write `random` after the number, it will be a random number in range from 0 to your set number")

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def feedSetMax(self, ctx, number:int, *useRandom):
        print(useRandom)
        if len(useRandom)>0 and useRandom[0] == "random":
            self.feedMax = random.randint(0, number)
        else:
            self.feedMax = number
            
        if self.feedMax <= self.feedCurrent:
            await ctx.send("The max feed was set to lower than current feed, resetting current values")
            self.feedCurrent = 0
            self.isOverfed = False
        

    @commands.command()
    async def feed(self, ctx):
        if self.feedCurrent < self.feedMax and not self.isOverfed:
            self.feedCurrent += 1
            if self.feedCurrent == self.feedMax:
                await self.sendFoodComaEmbed(ctx)
                self.isOverfed = True
                # How many seconds before it's ready. Random every time between a and b (120, 300)
                await asyncio.sleep(random.randint(120, 300)) 
                if self.isOverfed == True:
                    await self.feedReset(ctx)
            else:
                await self.sendFeedEmbed(ctx)
        else:
            await self.sendFoodComaEmbed(ctx)

def setup(client):
    client.add_cog(feeding(client))

