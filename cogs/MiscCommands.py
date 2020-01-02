import discord
from discord.ext import commands


class MiscCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

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
                         icon_url='https://cdn.discordapp.com/attachments/640127172148985861/661150910055186472/spider.png')
        embed.add_field(name='8ball', value="8ball can tell you your fortune if you ask it a question!\n"
                                            "Make sure to do **.8ball [Insert question]**", inline=False)
        embed.add_field(name='About', value="Make sure to do **.about**", inline=False)
        embed.add_field(name='Current Prefix', value="Make sure to type **prefix**", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def about(self, ctx):
        embed = discord.Embed(
            description="My name is **Scarlett**. I'm named after the Scarlet Spider in the Spiderman comics."
                        "Though, in this world, I'm just a bot who can be used to play games or play music! "
                        "Even though it seems like a little bit now, but later on I'll be able to provide you with"
                        "adventure games!",
            colour=discord.Colour.purple()
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/640127172148985861/661150910055186472/spider.png")
        embed.set_author(name="Scarlett",
                         icon_url='https://cdn.discordapp.com/attachments/640127172148985861/661150910055186472/spider.png')
        embed.add_field(name='Help', value="Try doing **.help**", inline=False)
        embed.add_field(name='Music', value="To get started, do **.play**", inline=False)
        embed.add_field(name='Games', value="Try doing **.games**", inline=False)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(MiscCommands(client))
