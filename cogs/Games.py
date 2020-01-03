import discord
from discord.ext import commands

import random


class Games(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question=None):
        if question is None:
            await ctx.send(f"You need to ask a question!")
        else:
            # good responses
            responses = ['It is certain.',
                         'It is decidedly so.',
                         'Without a doubt.',
                         'Yes-definitely.',
                         'You may rely on it.',
                         'As I see it, yes.',
                         'Most likely.',
                         'Outlook good.',
                         'Yes.',
                         'Signs points to yes.',
                         # neutral responses
                         'Reply hazy, try again.',
                         'Ask again later.',
                         'Better not tell you now.',
                         'Cannot predict now.',
                         'Concentrate and ask again.',
                         # negative responses
                         "Don't count on it.",
                         'My reply is no.',
                         'My sources say no.',
                         'Outlook not so good.',
                         'Very doubtful']
            await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")


def setup(client):
    client.add_cog(Games(client))
