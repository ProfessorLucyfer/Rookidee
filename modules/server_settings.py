from discord.ext import commands
from discord.ext.commands import Cog
import json, discord

settings = 'main/data/settings.json'
standard_prefix = "."

def json_open(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data


def json_write(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


class server_settings(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def ferro_say(self, ctx, channel:discord.TextChannel, *, msg:str):
        try:
            await channel.send(msg)
        except:
            await ctx.channel.send("Error sending the message. Could be permission issue...")


    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def edit_message(self, ctx, msg_old:discord.Message, msg_new:discord.Message):
        await msg_old.edit(content=msg_new.content)
    

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def ferro_react(self, ctx, msg:discord.Message,*, reactions):
        reactions_list = reactions.split(" ")
        print(reactions_list)
        for i in reactions_list:
            print(i)
            try:
                await msg.add_reaction(i)
                print("reacted")
            except:
                print(f"couldn't react with {i}")


    #### Prefix settings
    @Cog.listener("on_message")
    @commands.has_permissions(administrator=True)
    async def reset_prefix(self, message):
        """Reset the server prefix, will work no matter what prefix is set"""
        if message.author == self.client.user:
            return
        if message.guild == None:
            await message.author.send("Hi, I do not have any commands for use in DM")
            return

        if message.author.guild_permissions.administrator == True and message.content == "fb!reset":
            data = json_open(settings)
            guild_dict = data[str(message.guild.id)]
            guild_dict["prefix"] = standard_prefix
            data[str(message.guild.id)] = guild_dict
            json_write(settings, data)
            await message.channel.send("Prefix has been reset to fb!. To change it, use fb!change_prefix")



    @Cog.listener("on_message")
    async def pingForPrefix(self, message):
        """Ping ferro to see prefix"""
        if message.author == self.client.user:
            return
        if message.guild == None:
            await message.author.send("Hi, I do not have any commands for use in DM")
            return
        
        if (self.client.user in message.mentions) and (len(message.content.split(" ")) < 2):
            data = json_open(settings)
            guild_dict = data[str(message.guild.id)]
            prefix = guild_dict["prefix"]
            await message.channel.send(f"My prefix is currently `{prefix}`")

    @Cog.listener("on_guild_join")
    async def new_guild_prefix(self, guild):
        """Create guild_dict when bot joins new server"""
        data = json_open(settings)
        data[str(guild.id)] = {
            "prefix":standard_prefix,
            "welcome_channel":None
        }
        json_write(settings, data)




    @Cog.listener("on_guild_remove")
    async def remove_guild_prefix(self, guild):
        """Remove guild_dict when bot leaves a server"""
        data = json_open(settings)
        data.pop(str(guild.id))
        json_write(settings, data)
    

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def change_prefix(self, ctx, prefix:str=standard_prefix):
        """Customize prefix for the server"""
        data = json_open(settings)
        guild_dict = data[str(ctx.guild.id)]
        guild_dict["prefix"] = prefix
        data[str(ctx.guild.id)] = guild_dict
        json_write(settings, data)
        await ctx.send(f"Prefix changed to {prefix}")


    #### Member Welcome
    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def set_welcome(self, ctx, channel:discord.TextChannel=None):
        """Set welcome channel for the server"""
        data = json_open(settings)
        guild_dict = data[str(ctx.guild.id)]
        if channel:
            guild_dict["welcome_channel"] = str(channel.id)
        else:
            guild_dict["welcome_channel"] = None
        data[str(ctx.guild.id)] = guild_dict
        json_write(settings, data)
        await ctx.send(f"Welcome channel set to {channel}")


    @Cog.listener("on_member_join")
    async def member_welcome(self, member):
        """If welcome channel is set, welcome message will be sent there"""
        print(f"{member.name} joined {member.guild.name}")
        if member.guild.id == 703106165977907220:
            return
        data = json_open(settings)
        print(member.name)
        if str(member.guild.id) in list(data.keys()):
            guild_dict = data[str(member.guild.id)]
            if guild_dict["welcome_channel"]:
                welcome_channel = member.guild.get_channel(int(guild_dict["welcome_channel"]))
                embed = discord.Embed(colour=0x62eb96)
                embed.add_field(name='Someone new joined the server!', value=f"Please welcome {member.mention}")
                message = await welcome_channel.send(embed=embed)
                await message.add_reaction("<a:RHype:708568633508364310>")


def setup(client):
    client.add_cog(server_settings(client))