import random

import discord
from discord.ext import commands

from cogs import Levels


class MiscCommands(commands.Cog):

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

    @commands.command(aliases=["git", "gh"])
    async def github(self, ctx):
        await ctx.send("https://github.com/JustCasuallyJames")

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            description="Here are all the functions that I provide!",
            colour=discord.Colour.purple()
        )
        embed.set_author(name="Scarlett",
                         icon_url='https://cdn.discordapp.com/attachments/381281623246897162/665349252775411722/discord-scarlett.png')
        embed.add_field(name='8ball', value="8ball can tell you your fortune if you ask it a question!\n"
                                            "Make sure to do **.8ball [Insert question]**", inline=False)
        embed.add_field(name='About', value="Make sure to do **.about**", inline=False)
        embed.add_field(name='Current Prefix', value="Make sure to type **prefix**", inline=False)
        embed.add_field(name='Daily', value="Make sure to type **.daily**", inline=False)
        embed.add_field(name='Profile', value="Make sure to type **.profile** to see your stats!", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def about(self, ctx):
        embed = discord.Embed(
            description="My name is **Scarlett**. I'm named after the Scarlet Spider in the Spiderman comics."
                        "Though, in this world, I'm just a bot who can be used to play games or play music! "
                        "Even though it seems like a little bit now, but later on I'll be able to provide you with"
                        " adventure games!",
            colour=discord.Colour.purple()
        )
        embed.set_author(name="Scarlett",
                         icon_url='https://cdn.discordapp.com/attachments/381281623246897162/665349252775411722/discord-scarlett.png')
        embed.add_field(name='Help', value="Try doing **.help**", inline=False)
        embed.add_field(name='Music', value="To get started, do **.play**", inline=False)
        embed.add_field(name='Games', value="Try doing **.games**", inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=["stats"])
    async def profile(self, ctx):
        level = await self.client.pg_con.fetchval(
            # LIMIT 1 is necessary for SELECT statements so no duplicate records
            """
            SELECT lvl FROM levels.users
            WHERE user_id = $1 AND guild_id = $2
            LIMIT 1
            """, ctx.message.author.id, ctx.message.guild.id
        )
        xp = await self.client.pg_con.fetchval(
            """
            SELECT xp FROM levels.users 
            WHERE user_id = $1 AND guild_id = $2
            LIMIT 1
            """, ctx.message.author.id, ctx.message.guild.id
        )
        money = await self.client.pg_con.fetchval(
            """
            SELECT money FROM money.bank
            WHERE user_id = $1 AND guild_id = $2
            LIMIT 1
            """, ctx.message.author.id, ctx.message.guild.id
        )
        embed = discord.Embed(
            author=f"{ctx.message.author.name}",
            colour=discord.Colour.blue()
        )
        embed.set_author(name= f"{ctx.message.author.name}", icon_url=f"{ctx.message.author.avatar_url}")
        embed.set_thumbnail(
            url=f"{ctx.message.author.avatar_url}")
        embed.add_field(name='Level', value=f"{level}", inline=True)
        embed.add_field(name='XP',
                        value=f"Current exp: {xp-Levels.lvltoxp(level)} out of {Levels.lvltoxp(level+1)-Levels.lvltoxp(level)}",
                        inline=True)
        embed.add_field(name='Wallet',
                        value=f"{money} coins",
                        inline=False)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(MiscCommands(client))
