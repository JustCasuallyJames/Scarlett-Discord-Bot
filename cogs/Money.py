import discord
from discord.ext import commands


class Money(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def get_coins(self, member_id, guild_id):
        return await self.client.pg_con.fetchval(
            f"""
            SELECT money FROM money.bank
            WHERE user_id = {member_id} AND guild_id = {guild_id}
            LIMIT 1
            """
        )

    async def add_coins(self, member_id, guild_id, coins):
        await self.client.pg_con.execute(
            """
            UPDATE money.bank SET money = money + $1
            WHERE user_id = $2 AND guild_id = $3
            """, coins, member_id, guild_id
        )
        return await self.get_coins(member_id, guild_id)

    async def sub_coins(self, member_id, guild_id, points):
        return await self.add_coins(member_id, guild_id, -points)

    @commands.command(aliases=["DAILY"])
    @commands.cooldown(1, 1080, commands.BucketType.user)
    async def daily(self, ctx):
        await self.client.pg_con.execute(
            # add a multiplier later...
            """
            INSERT INTO money.bank(guild_id, user_id, money,daily_streak)
            VALUES ($1, $2, 20, 0)
            ON CONFLICT (user_id, guild_id) DO
            UPDATE SET money = bank.money + $3, daily_streak = bank.daily_streak + 1 
            """, ctx.message.guild.id, ctx.message.author.id, 20
        )
        streak = await self.client.pg_con.fetchval(
            """
            SELECT daily_streak FROM money.bank
            WHERE user_id = $1 AND guild_id = $2
            LIMIT 1
            """, ctx.message.author.id, ctx.message.guild.id
        )
        await self.client.pg_con.execute(
            """
            UPDATE money.bank SET money = bank.money + $3
            WHERE user_id = $1 AND guild_id = $2
            """, ctx.message.author.id, ctx.message.guild.id, streak * 5
        )
        daily_money = 20 + (streak * 5)
        await ctx.send(f"{ctx.message.author.mention} has collected their daily amount of **{daily_money} coins.**")

    @commands.command()
    async def give(self, ctx, member: discord.Member, *, money: int):
        member_giver = ctx.message.author
        guild_id_giver = ctx.message.guild.id
        bank = await self.get_coins(member_giver.id, guild_id_giver)
        if money > bank or money == 0:
            await ctx.send("You have insufficient funds.")
            return
        if member.bot:
            await ctx.send("You can't give money to bots.")
            return
        if member_giver.id is member.id:
            await ctx.send("You can't give money to yourself.")
            return
        await self.add_coins(member.id, member.guild.id, money)
        await self.sub_coins(member_giver.id, guild_id_giver, money)
        return await ctx.send(f"{member_giver.mention} has given {member.mention} {money} coins!")

    @commands.command()
    @commands.is_owner()
    async def addmoney(self, ctx, member: discord.Member, *, money: int):
        await self.client.pg_con.execute(
            """
            UPDATE money.bank SET money = bank.money + $1 
            WHERE user_id = $2 AND guild_id = $3
            """, money, member.id, member.guild.id
        )
        return await ctx.send(f"{member.mention} was given {money} coins")


def setup(client):
    client.add_cog(Money(client))
