import discord
import os
import datetime
import asyncio
from discord.ext import commands


class moderation(commands.Cog): 
    def __init__(self, client):
        self.client = client
        self.guild = discord.Client.get_guild(self.client, 848346057767256076)
        self.muteRole = discord.utils.get(self.guild.roles, name="Muted")
        self.trademuteRole = discord.utils.get(self.guild.roles, name="Trade Muted")
        self.modLogsChannel = discord.utils.get(self.guild.channels, name="🔨┃mod-logs")

    @commands.command(name = 'purge', aliases=['clear', 'clean', 'p', 'c'])
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx, amount=2):
        await ctx.channel.purge(limit=amount)
    
    @commands.command()
    @commands.has_permissions(manage_roles = True)
    async def smute (self, ctx, member: discord.Member, time, d, *, reason="None"):

        await member.add_roles(self.muteRole)
        embed = discord.Embed(title="User Muted:", description=f"{member.mention} has been muted.", colour=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Reason:", value=reason, inline=False)
        embed.add_field(name="Mute Duration Remaining", value=f"{time}{d}", inline=False)
        await self.modLogsChannel.send(embed=embed)
        await member.send(f"You have been muted for {reason} for {time}{d}")
        if d == "s":
            await asyncio.sleep(int(time))
        if d == "m":
            await asyncio.sleep(int(time*60))
        if d == "h":
            await asyncio.sleep(int(time*60*60))
        if d == "d":
            await asyncio.sleep(int(time*60*60*24))
        await member.remove_roles(self.muteRole)
        embed = discord.Embed(title="User Unmuted:", description=f"Unmuted {member.mention}", colour=discord.Colour.green(), timestamp=datetime.datetime.utcnow())
        await self.modLogsChannel.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unsmute (self, ctx, member: discord.Member):

        await member.remove_roles(self.muteRole)
        embed = discord.Embed(title="User Unmuted:", description=f"Unmuted {member.mention}", colour=discord.Colour.green(), timestamp=datetime.datetime.utcnow())
        await self.modLogsChannel.send(embed=embed)
        await member.send(f"You have been unmuted from: {self.guild}")

    @commands.command()
    @commands.has_permissions(manage_roles = True)
    async def tmute (self, ctx, member: discord.Member, time, d, *, reason="None"):

        embed = discord.Embed(title="User Trade-Muted:", description=f"{member.mention} was trade muted.", colour=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Reason:", value=reason, inline=False)
        await self.modLogsChannel.send(embed=embed)
        await member.add_roles(self.trademuteRole, reason=reason)
        await member.send(f"You have been trade-muted for {reason}.")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def untmute (self, ctx, member: discord.Member):

        await member.remove_roles(self.trademuteRole)
        embed = discord.Embed(title="User Unmuted:", description=f"Unmuted {member.mention}", colour=discord.Colour.green(), timestamp=datetime.datetime.utcnow())
        await self.modLogsChannel.send(embed=embed)
        await member.send(f"You have been un-trade-muted from: {self.guild}")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No Reason"):
        if member == None:
            embed = discord.Embed(f"{ctx.message.author}, Please enter a valid user!")
            await ctx.reply(embed=embed)

        else:
            embed = discord.Embed(title="User Kicked:", description=f"{member.mention} has been kicked.", colour=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Reason: ", value=reason, inline=False)
            await self.modLogsChannel.send(embed=embed)
            await member.send(f"You have been kicked from The Rookery. Reason: {reason}.")
            await self.guild.kick(user=member)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No Reason"):
        if member == None:
            embed = discord.Embed(f"{ctx.message.author}, specify a valid user.")
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(title="User Banned:", description=f"{member.mention} has been banned.", colour=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Reason: ", value=reason, inline=False)
            await self.modLogsChannel.send(embed=embed)
            await member.send(f"You have been banned from The Rookery. Reason: {reason}.")
            await self.guild.ban(user=member)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def unban(self, ctx, user: discord.User):
        if user == None:
            embed = discord.Embed(f"{ctx.message.author}, specify a valid user ID.")
            await ctx.reply(embed=embed)

        else:
            embed = discord.Embed(title="User Unbanned:", description=f"{user.display_name} has been unbanned.", colour=discord.Colour.green(), timestamp=datetime.datetime.utcnow())
            await self.modLogsChannel.send(embed=embed)
            await self.guild.unban(user=user)

async def setup(client):
    await client.add_cog(moderation(client))