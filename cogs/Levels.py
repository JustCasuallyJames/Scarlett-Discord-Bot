import discord
from discord.ext import commands

import math


class Levels(commands.Cog):

    def __init__(self, client):
        self.client = client

    def xptolvl(self, xp):
        return math.floor(math.pow((5 / 4) * xp, 1 / 3))

    def lvltoxp(self, lvl):
        return round((4 / 5) * math.pow(lvl, 3))

    async def lvl_up(self, xp, lvl):
        if lvl % 2 != 0:
        # showing odds
            return xp == self.lvltoxp(lvl)
        else:
        # showing evens
            return xp == self.lvltoxp(lvl)+1

    @commands.Cog.listener()
    # release notes tmmr
    async def on_message(self, message):
        if message.author.bot:
            return

        xp = await self.client.pg_con.fetchval(
            """
            INSERT INTO public.users(user_id, guild_id, xp, lvl)
            VALUES ($1, $2, 0, 1)
            ON CONFLICT (user_id, guild_id) DO
            UPDATE SET xp = users.xp + 1 
            RETURNING xp
            """, message.author.id, message.guild.id
        )
        lvl = math.floor(math.pow((5 / 4) * xp, 1 / 3))
        next_lvl_xp = round((4 / 5) * math.pow(lvl + 1, 3))
        print(f"{message.author.name} next lvl exp: {next_lvl_xp}")
        print(f"{message.author.name} exp: {xp}")
        print(f"{message.author.name} lvl: {math.floor(math.pow((5 / 4) * xp, 1 / 3))}")
        if await self.lvl_up(xp, lvl):
            await self.client.pg_con.execute("UPDATE users SET lvl = $1 WHERE user_id = $2 AND guild_id =$3",
                                             math.floor(math.pow((5 / 4) * xp, 1 / 3)), message.author.id, message.guild.id)
            await message.channel.send(f"{message.author.mention} is now level {lvl}")


def setup(client):
    client.add_cog(Levels(client))
