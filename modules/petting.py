import discord, asyncio
import numpy as np
from discord.ext import commands
from discord.ext.commands import Cog, CommandOnCooldown
from discord.ext.commands.cooldowns import BucketType
from .server_settings import json_write, json_open
import random, re, sys


pet_count_path = 'data/pet_count.json'
settings = 'data/settings.json'

class petting(commands.Cog):
    def __init__(self, client):
        self.client = client

    @Cog.listener("on_guild_join")
    async def guild_add(self, guild):
        data = json_open(pet_count_path)
        data[str(guild.id)] = {
            "pet_stat":"random",
            "chance":0.75,
            "Total pet":0,
            "Total hurt":0,
            "Members":{}
        }
        json_write(pet_count_path, data)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def pet_random(self, ctx):
        embed = discord.Embed()
        embed.add_field(name="Would you like to always allow pets?", value="React with ✅ to always allow\nReact with ❌ to set to random")
        message = await ctx.send(embed=embed)

        emoji_list = ['✅','❌']
        data = json_open(pet_count_path)
        guild_settings = data[str(ctx.guild.id)]
        for i in emoji_list:
            await message.add_reaction(i)

        def checker(reaction, user):
            return user == ctx.author and str(reaction.emoji) in emoji_list

        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=15, check=checker)

                if str(reaction.emoji) == "✅":
                    guild_settings["pet_stat"] = "always"
                    await ctx.send("Pet settings changed to always allow pets")
                elif str(reaction.emoji) == "❌":
                    guild_settings["pet_stat"] = "random"
                    await ctx.send("Pet settings changed to randomize pets")

                data[str(ctx.guild.id)] = guild_settings
                json_write(pet_count_path, data)
                await message.delete()
                    
            except asyncio.TimeoutError:
                break

    @commands.command(description="Give Rookidee a pet, he loves his feathers ruffled!")
    async def pet(self, ctx):
        data = json_open(pet_count_path)
        guild_dict = data[str(ctx.guild.id)]
        random = guild_dict["pet_stat"]
        Member_dict = guild_dict["Members"]
        if str(ctx.author.id) in Member_dict.keys():
            member = Member_dict[str(ctx.author.id)]
        else:
            Member_dict[str(ctx.author.id)] = {"pet":0, "hurt":0}
            member = Member_dict[str(ctx.author.id)]
        
        if random == "random":
            choices = ['pet', 'no pet']
            pet_chance = float(guild_dict["chance"])
            hurt_chance = float(1 - pet_chance)
            selection = np.random.choice(choices, 1, p=[pet_chance, hurt_chance])
        elif random == "always":
            selection = ['pet']

        if selection[0] == 'pet':
            total_pet = guild_dict["Total pet"]
            total_pet += 1
            guild_dict["Total pet"] = total_pet
            pet_count = member["pet"]
            pet_count += 1
            member["pet"] = pet_count
            embed = discord.Embed(
            colour = discord.Colour.green())
            embed.add_field(name='Rookidee knew this day would come!', value=f"{ctx.author.mention} pet Rookidee! <:rookihapp:988570898602790952> \n"
                                                                        "\nYou have given me pets **"+str(pet_count)+"x** times!")

        elif selection[0] == 'no pet':
            total_hurt = guild_dict["Total hurt"]
            total_hurt += 1
            guild_dict["Total hurt"] = total_hurt
            pet_hurt = member["hurt"]
            pet_hurt += 1
            member["hurt"] = pet_hurt
            embed = discord.Embed(
            colour = discord.Colour.red())
            embed.add_field(name='*Sorry!*', value=f"{ctx.author.mention} got pecked on the hand! <:rookiangy:988570921814073374>\n"
                                                    "\nI've hurt you a total of **"+ str(pet_hurt) +"x** times.")

        Member_dict[str(ctx.author.id)] = member
        guild_dict["Members"] = Member_dict
        data[str(ctx.guild.id)] = guild_dict
        json_write(pet_count_path, data)
        await ctx.send(embed=embed)

    @pet.error
    async def pet_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            time = str(int(error.retry_after))
            await ctx.send(f"You can't pet me this often, you need to wait {time}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def pet_chance(self, ctx, value:float=0.75):
        """Change % chance of petting/getting hurt"""
        data = json_open(pet_count_path)
        guild_dict = data[str(ctx.guild.id)]
        if value>=1 or value<0:
            await ctx.send("Enter a value between 0 and 1")
        else:
            guild_dict["chance"] = value
            data[str(ctx.guild.id)] = guild_dict
            json_write(pet_count_path, data)
            value = value*100
            value = int(value)
            await ctx.send(f"Rookidee has now **{value}%** chance of getting pet")


    @commands.command()
    async def pets_total(self, ctx):
        """Show server total pet and hurt count"""
        data = json_open(pet_count_path)
        guild_dict = data[str(ctx.guild.id)]
        petcount = str(guild_dict["Total pet"])
        hurtcount = str(guild_dict["Total hurt"])
        embed = discord.Embed(colour=discord.Colour.green())
        embed.add_field(name=f"Hi {ctx.guild.name}", value="These are pet/hurt stats for this server!")
        embed.add_field(name="Total times pet on this server:", value=f"**{petcount}x** times", inline=False)
        embed.add_field(name="Total time I've hurt someone on this server", value=f"**{hurtcount}x** times", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def pets(self, ctx):
        """Show personal pet and hurt count"""
        data = json_open(pet_count_path)
        guild_dict = data[str(ctx.guild.id)]
        Member_dict = guild_dict["Members"]
        if str(ctx.author.id) in Member_dict.keys():
            user_dict = Member_dict[str(ctx.author.id)]
            pet = str(user_dict["pet"])
            hurt = str(user_dict["hurt"])
            allowed_mentions = discord.AllowedMentions(users=False)
            await ctx.send(f"{ctx.author.mention}! you have pet me **{pet}x** times, and have been hurt **{hurt}x** times.", allowed_mentions=allowed_mentions)

    @commands.command(pass_context=True, name = 'bonk', aliases=['unfeed', 'boop'])
    async def bonk(self, ctx):
        id = ctx.message.author.id
        embed = discord.Embed(
        colour = discord.Colour.red())
        embed.add_field(name='You have been attacked!', value="<@"+str(id)+"> was viciously attacked by Rookidee!")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def dance(self, ctx):
        choice = [1,2,3,4,5,6,7,8,9,10]
        selection = random.choice(choice)
        if selection <= 7:
            embed = discord.Embed(
            colour = discord.Colour.green())
            embed.add_field(name='Rookidee used Feather Dance!', value="Rookidee lowered your attack greatly! \n" 
                                                                            "\n Rookidee enjoyed his dance!")
            await ctx.send(embed=embed)
        elif 8<= selection <= 9:
            embed = discord.Embed(
            colour = discord.Colour.green())
            embed.add_field(name='Rookidee used... Swords Dance?!', value="Rookidee's Attack was raised greatly! \n" 
                                                                            "\n Rookidee enjoyed his dance!")
            await ctx.send(embed=embed)
        elif selection >= 10:
            embed = discord.Embed(
            colour = discord.Colour.green())
            embed.add_field(name='Rookidee used... Dragon Dance?!', value="Rookidee's Attack and Speed were raised! \n" 
                                                                            "\n Rookidee enjoyed his dance!")
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(petting(client))  