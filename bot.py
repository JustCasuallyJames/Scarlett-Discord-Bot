import discord
from discord.ext import commands

import json
import os

import discordKey


# Make an array of tuples, by name and then command function, and use that to call the commands in your message event
async def get_prefix(client, message):
    # del client
    if message.guild is None:
        return '.'

    with open('data/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    # if theres nothing in the file, it will be a . until changed
    return prefixes.get(str(message.guild.id), '.')


client = commands.Bot(command_prefix=get_prefix, activity=discord.Game(name=".help"))
client.remove_command('help')


@client.command()
@commands.is_owner()
async def load(ctx, extension):
    try:
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f"Loaded {extension}")
    except commands.ExtensionNotLoaded:
        await ctx.send(f"{extension} was not properly loaded.")
    except commands.ExtensionNotFound:
        await ctx.send(f"{extension} was deleted and could not be found.")
    except commands.NoEntryPointError:
        await ctx.send(f"{extension} is missing a setup function.")
    except commands.ExtensionFailed:
        await ctx.send(f"{extension} has an error in the setup function.")


@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    try:
        client.unload_extension(f'cogs.{extension}')
        await ctx.send(f"unloaded {extension}")
    except commands.ExtensionNotLoaded:
        await ctx.send(f"{extension} was not properly loaded.")


@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    try:
        client.reload_extension(f'cogs.{extension}')
        await ctx.send(f"Reloaded: {extension}")
    except commands.ExtensionNotLoaded:
        await ctx.send(f"{extension} was not properly loaded.")
    except commands.ExtensionNotFound:
        await ctx.send(f"{extension} was deleted and could not be found.")
    except commands.NoEntryPointError:
        await ctx.send(f"{extension} is missing a setup function.")
    except commands.ExtensionFailed:
        await ctx.send(f"{extension} has an error in the setup function.")


for filename in os.listdir("./cogs"):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(discordKey.key)
