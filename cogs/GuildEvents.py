import discord
from discord.ext import commands

import json


class GuildEvents(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # This doesn't show the bot joining because it can't consider itself joining
        print(f'{member} has joined the server.')
        if member.bot:
            return
        role = discord.utils.get(member.guild.roles, name='Casual Crew')
        await member.add_roles(role)
        channel = member.guild.get_channel(661163292311552040)
        embed = discord.Embed(
            title="**Welcome**",
            description=f"{member.mention} just joined our server!",
            colour=discord.Colour.green()
        )
        embed.set_thumbnail(
            url=f"{member.avatar_url}")
        embed.set_footer(text=f"ID: {member.id}")
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} has left the server.')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open('data/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(guild.id)] = '.'

        with open('data/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open('data/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes.pop(str(guild.id))

        with open('data/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)


def setup(client):
    client.add_cog(GuildEvents(client))
