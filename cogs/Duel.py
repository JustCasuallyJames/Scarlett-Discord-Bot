import random

import discord
from discord.ext import commands


class Duel(commands.Cog):

    def __init__(self, client):
        self.client = client

    def grant_sword(self):
        return random.choice([True, False])

    def grant_health(self):
        return random.choice([True, False])

    def list_attcks(self, member1: discord.Member, member2: discord.Member):
        return random.choice([f"{member1.mention} stabs {member2}.",
                              f"{member1.mention} cuts off {member2} arm.",
                              f"{member1.mention} cuts off {member2} leg.",
                              f"{member1.mention} takes a jab at {member2}.",
                              f"{member1.mention} jumps and deals a powerful slice to {member2}"])

    async def turn(self,ctx,user: discord.User):
        return await ctx.send(f"It is {user.mention}'s turn.")

    @commands.command()
    async def duel(self, ctx, user: discord.User, *, bet: int):
        player_1 = ctx.message.author
        player_1_health = 10
        player_1_attack = 1
        player_2 = user.name
        player_2_health = 10
        player_2_attack = 1
        cog = self.client.get_cog("Money")
        bank = await cog.get_coins(player_1, ctx.message.guild.id)

        if bet > bank or bet == 0:
            await ctx.send("You have insufficient funds.")
            return

        self.turn(ctx, player_1)
        if ctx.message.content.find("attack"):
            player_2_health -= player_1_health






def setup(client):
    client.add_cog(Duel(client))
