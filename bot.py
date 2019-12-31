import os
import discordKey
import discord
from discord.ext import commands
import json


# Make an array of tuples, by name and then command function, and use that to call the commands in your message event

async def get_prefix(client, message):
    # del client
    if message.guild is None:
        return '.'

    with open('cogs/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    # if theres nothing in the file, it will be a . until changed
    return prefixes.get(str(message.guild.id), '.')


client = commands.Bot(command_prefix=get_prefix)
client.remove_command('help')


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f"Loaded {extension}")


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f"unloaded {extension}")


for filename in os.listdir("./cogs"):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(discordKey.key)
