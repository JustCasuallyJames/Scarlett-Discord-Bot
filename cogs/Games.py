import random

import discord
from discord.ext import commands


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

    @commands.command()
    async def coinflip(self, ctx, choice: str, *, gamble: int):
        member = ctx.message.author
        guild_id = ctx.message.guild.id
        cog = self.client.get_cog("Money")
        bank = await cog.get_coins(member.id, guild_id)

        HEAD_CHOICES = ("Heads", "heads", "h", "hd", "head")
        TAIL_CHOICES = ("Tails", "tails", "t", "tl", "tail")
        # 1 is heads 0 is tails
        if gamble > bank or gamble == 0:
            await ctx.send("You have insufficient funds.")
            return

        winning_answers = random.choice([HEAD_CHOICES, TAIL_CHOICES])
        if choice in winning_answers:
            await cog.add_coins(member.id, guild_id, gamble)
            await ctx.send(f"Flip: {winning_answers[0]}. You won {gamble} coins!")
        else:
            await cog.sub_coins(member.id, guild_id, gamble)
            await ctx.send(f"Flip: {winning_answers[0]}. You lost {gamble} coins!")


def setup(client):
    client.add_cog(Games(client))
