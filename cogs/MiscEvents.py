import discord
from discord.ext import commands

import json
import sys
import traceback


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
        if message.content.startswith('mc'):
            await message.channel.send('No fuck you')
        if message.content.startswith('pepega'):
            await message.channel.send("Yes we know you're pepega..")
        if message.content.startswith('prefix'):
            await message.channel.send(f"\nThe current prefix is: {prefixes[str(message.author.guild.id)]}")


def setup(client):
    client.add_cog(MiscEvents(client))
