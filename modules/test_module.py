import discord
from discord.ext import commands
from discord.ext.commands import Cog

class test_module(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Command registered, latency: {str(round(self.client.latency, 4))}")
        
async def setup(client):
    await client.add_cog(test_module(client))