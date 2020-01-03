import discord
from discord.ext import commands


class Money(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def daily(self, ctx):
        money = await self.client.pg_con.fetchval(
            """
            INSERT INTO money.bank(guild_id, user_id, money)
            VALUES ($1, $2, 10)
            ON CONFLICT (user_id, guild_id) DO
            UPDATE SET money = bank.money + 20 
            RETURNING money
            """, ctx.message.guild.id, ctx.message.author.id
        )
        await ctx.send(f"{ctx.message.author.mention} has collected their daily amount of **{money} coins.**")


def setup(client):
    client.add_cog(Money(client))
