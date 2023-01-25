import discord
intents = discord.Intents.all()
from discord.ext import commands
import json

def get_prefix(client, message):
    with open(prefix_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        guild_dict = data[str(message.guild.id)]
    return guild_dict["prefix"]

def ext_modules_open():
    with open('data/ext_modules.json') as f:
        modules = json.load(f)
        return modules
        
def ext_modules_write(data):
    with open('data/ext_modules.json') as f:
        json.dump(data, f)

TOKEN = open("data/token.txt", "r").readline()
prefix_path = 'data/settings.json'
client = commands.Bot(
    command_prefix = (get_prefix),
    intents = intents)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        await client.process_commands(message)


@client.event
async def on_ready():
    loaded_modules = []
    not_loaded_modules = []
    print(f"logged in as {client.user.name}\nID: {client.user.id}")
    print("\n--------\nLoading modules")
    modules = ext_modules_open()
    for i in modules:
        try:
            client.load_extension('modules.'+i)
            loaded_modules.append(i)
        except Exception as error:
            print(f"Could not load module {i}")
            print(f"{i} {error}")
            not_loaded_modules.append(i)
    
    print("Loaded modules: "+ ', '.join(i for i in loaded_modules))
    print("Modules not loaded: "+ ', '.join(i for i in not_loaded_modules))

@client.command()
async def set_game(ctx, a=None):
    activity = discord.Game(a)
    await client.change_presence(activity=activity)


@client.command()
async def stop_game(ctx):
    await client.change_presence(activity=None)


@client.command()
async def set_watching(ctx, w=None):
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=w))

@client.command()
@commands.is_owner()
async def role_kick(ctx, role: discord.Role):
    [await member.kick() for member in ctx.guild.members if role in member.roles]

@client.command(hidden=True)
@commands.is_owner()
async def extension(ctx, task:str=None, module:str=None):
    """Command to add, remove or load/unload extensions"""
    modules = ext_modules_open()
    if task == "names":
        await ctx.send(', '.join(i for i in modules))
    elif task == "add":
        modules.append(module)
        ext_modules_write(modules)
    elif task == "remove":
        modules.pop(module)
        ext_modules_write(modules)
        
    if task=='load':
        try:
            if module=='petting':
                client.load_extension(module)
            else:
                client.load_extension('modules.'+module)
            print(f"{module} has been loaded")
            await ctx.send(f"{module} has been loaded")
        except Exception as error:
            print(f"Unable to load {module}\nError: {error}")
            await ctx.send(f"Unable to load {module}\nError: {error}")
    elif task=='unload':
        if module=='BotSettings':
            await ctx.send(f"Cannot unload {module}. This module only supports \"reload\"")
            return
        try:
            if module=='petting':
                client.unload_extension(module)
            else:
                client.unload_extension('modules.'+module)
            print(f"{module} has been unloaded")
            await ctx.send(f"{module} has been unloaded")
        except Exception as error:
            print(f"Unable to unload {module}\nError: {error}")
            await ctx.send(f"Unable to unload {module}\nError: {error}")
    elif task == "reload":
        try:
            if module=='petting':
                client.reload_extension(module)
            else:
                client.reload_extension('modules.'+module)
            print(f"Reloaded {module}")
            await ctx.send(f"Reloaded {module}")
        except Exception as error:
            print(f"Unable to reload {module}\nError: {error}")
            await ctx.send(f"Unable to reload {module}\nError: {error}")

    
client.run(TOKEN)