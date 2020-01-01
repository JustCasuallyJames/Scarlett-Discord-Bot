import discord
from discord.ext import commands


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_role("Moderators")
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount + 1)


def setup(client):
    client.add_cog(Moderation(client))
