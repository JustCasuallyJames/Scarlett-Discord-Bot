import discord
from discord.ext import commands

import json

# from cogs.MiscCommands import switch
# from cogs.MiscCommands import MiscCommands

class MiscEvents(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is ready........")

    @commands.Cog.listener()
    async def on_message(self, message):
        with open('data/prefixes.json', 'r') as f:
            prefixes = json.load(f)
            #needed for when we want to get the current prefix of the discord server
        if message.content.startswith('mc'):
            await message.channel.send('No fuck you')
        if message.content.startswith('pepega'):
            await message.channel.send("Yes we know you're pepega..")
        if message.content.startswith('prefix'):
            await message.channel.send(f"\nThe current prefix is: {prefixes[str(message.author.guild.id)]}")
        if message.content.startswith('I need help!'):
            await message.channel.send(f"\nNo!")
        if message.content.startswith(f"I have a bug"):
            await message.channel.send('Just fix it then?')


def setup(client):
    client.add_cog(MiscEvents(client))
