import discord
from discord.ext import commands

import math


class Levels(commands.Cog):

    def __init__(self, client):
        self.client = client

    @staticmethod
    def xptolvl(xp):
        return math.floor(((5/4)*xp) ** (1/3))

    @staticmethod
    def lvltoxp(lvl):
        return math.ceil((4/5) * (lvl ** 3))

    async def is_lvl_up(self, xp, lvl):
        # 0 is false, 1 is true
        # used like binary
        # int(not(lvl % 2))
        return xp == self.lvltoxp(lvl)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        xp = await self.client.pg_con.fetchval(
            """
            INSERT INTO public.users(user_id, guild_id, lvl, xp)
            VALUES ($1, $2, 1, 1)
            ON CONFLICT (user_id, guild_id) DO
            UPDATE SET xp = users.xp + 1 
            RETURNING xp
            """, message.author.id, message.guild.id
        )
        lvl = self.xptolvl(xp)
        next_lvl_xp = self.lvltoxp(lvl+1)
        print(f"{message.author.name} next lvl exp: {next_lvl_xp}")
        print(f"{message.author.name} exp: {xp}")
        print(f"{message.author.name} lvl: {self.xptolvl(xp)}")
        if await self.is_lvl_up(xp, lvl):
            await self.client.pg_con.execute("UPDATE users SET lvl = $1 WHERE user_id = $2 AND guild_id =$3",
                                             self.xptolvl(xp), message.author.id,
                                             message.guild.id)
            await message.channel.send(f"{message.author.mention} is now level {lvl}")


def setup(client):
    client.add_cog(Levels(client))
