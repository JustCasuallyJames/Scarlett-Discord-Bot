import discord
from discord.ext import commands

import math
import decimal

decimal.getcontext().prec = 28


def xptolvl(xp):
    # number = (((5 / 4) * xp) ** 1 / 3) * 1000000000000000
    # whole_number = math.floor(((5 / 4) * xp) ** 1 / 3) * 1000000000000000
    # if number - whole_number == 999999999999999:
    #     print("working......")
    #     return math.ceil(((5 / 4) * xp) ** .3333333333333)
    return math.floor(((5/4)*xp)**(1/3))


def lvltoxp(lvl):
    return math.ceil((4 / 5) * (lvl ** 3))


class Levels(commands.Cog):

    def __init__(self, client):
        self.client = client

    def is_lvl_up(self, xp, lvl):
        return xp == lvltoxp(lvl)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.startswith("."):
            return

        xp = await self.client.pg_con.fetchval(
            """
            INSERT INTO levels.users(user_id, guild_id, lvl, xp)
            VALUES ($1, $2, 1, 1)
            ON CONFLICT (user_id, guild_id) DO
            UPDATE SET xp = users.xp + 1 
            RETURNING xp
            """, message.author.id, message.guild.id
        )
        lvl = xptolvl(xp)
        # print(f"lvl: {lvl}")
        await self.client.pg_con.execute(
            "UPDATE levels.users SET lvl = $1 "
            "WHERE user_id = $2 AND guild_id =$3",
            lvl, message.author.id, message.guild.id
        )
        # print(f"EXAMPLE: {lvltoxp(4)}")
        # print(f"EXAMPLE: {lvltoxp(5)}")
        # decimal.Decimal(((5 / 4) * xp) ** (1 / 3))
        print(f"1/3: {decimal.Decimal(1 / 3)}")
        print(f"ACTUAL LVL: {((5 / 4) * float(xp)) ** (1/3)}")
        print(f"XPTOLVL: {xptolvl(100)}")
        print(f"xp: {xp}")
        print(f"lvl: {xptolvl(xp)}")
        print(self.is_lvl_up(xp, lvl))
        if self.is_lvl_up(xp, lvl):
            await message.channel.send(f"{message.author.mention} is now level {lvl}")


def setup(client):
    client.add_cog(Levels(client))
