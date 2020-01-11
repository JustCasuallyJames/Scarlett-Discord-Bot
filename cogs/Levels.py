import discord
from discord.ext import commands

import math
import decimal

decimal.getcontext().prec = 28


def xptolvl(xp):
    return math.floor(((5 / 4) * xp) ** (1 / 3))


def lvltoxp(lvl):
    return math.ceil((4 / 5) * (lvl ** 3))


class Levels(commands.Cog):

    def __init__(self, client):
        self.client = client

    def is_lvl_up(self, xp, lvl):
        return xp == lvltoxp(lvl) + 1

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.startswith("."):
            return

        xp = await self.client.pg_con.fetchval(
            """
            INSERT INTO levels.users(user_id, guild_id, lvl, xp)
            VALUES ($1, $2, 0, 0)
            ON CONFLICT (user_id, guild_id) DO
            UPDATE SET xp = users.xp + 1 
            RETURNING xp
            """, message.author.id, message.guild.id
        )
        await self.client.pg_con.execute(
            f"""
            INSERT INTO money.bank(user_id, guild_id, money, daily_streak)
            VALUES ({message.author.id}, {message.guild.id}, 0, 0)
            ON CONFLICT (user_id, guild_id) DO
            UPDATE SET money = bank.money + 0 
            """
        )
        lvl = xptolvl(xp)
        await self.client.pg_con.execute(
            "UPDATE levels.users SET lvl = $1 "
            "WHERE user_id = $2 AND guild_id =$3",
            lvl, message.author.id, message.guild.id
        )
        LEVEL_UP_MONEY = 100
        if self.is_lvl_up(xp, lvl) and lvl > 0:
            await message.channel.send(f"{message.author.mention} is now level {lvl}\n"
                                       f"Upon leveling up, you've been granted {LEVEL_UP_MONEY} coins!")
            await self.client.pg_con.execute(
                "UPDATE money.bank SET money = bank.money + $1 WHERE user_id = $2 AND guild_id = $3",
                LEVEL_UP_MONEY, message.author.id, message.guild.id
            )


def setup(client):
    client.add_cog(Levels(client))
