import discord
from discord.ext import commands
import json
import random


class Commands(commands.Cog):

    def __init__(self, client):
        self.client = client

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

    @commands.command()
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount + 1)

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

    @commands.command(aliases=["changeprefix"])
    @commands.has_role("Moderators")
    async def changePrefix(self, ctx, prefix):
        with open('cogs/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        # role = discord.utils.get(ctx.author.roles, name="Moderators")
        # if role in ctx.author.roles:
        if len(prefix) == 1:
            prefixes[str(ctx.guild.id)] = prefix
        else:
            await ctx.send("You can't put a prefix that's more than one character!")
        # else:
        #     await ctx.send(f"Unfortunately, you can't change the prefix.")

        with open('cogs/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        embed = discord.Embed(
            description=f"The changed prefix is: {prefixes[str(ctx.guild.id)]}",
            colour=discord.Colour.purple()
        )
        # embed.set_author(name="Scarlett",
        #                  icon_url='https://cdn.discordapp.com/attachments/640127172148985861/661150910055186472/spider.png')
        await ctx.send(embed=embed)

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

    @commands.command(aliases=["addrole"])
    @commands.has_role("Moderators")
    # The * causes role to hold the user input text after the member name, including any interior whitespace.
    # This lets the user write the following to add the "My Little Pony" role to hogarth: .addrole @hogarth My Little Pony
    async def add_roles(self, ctx, member: discord.Member, *, role: discord.Role):
        # role = discord.utils.get(member.guild.roles, name=role_name)
        await member.add_roles(role)
        # await member.send(f"You've been awarded the **{role}** role")
        embed = discord.Embed(
            title="**Role added**",
            description=f"{member.mention} awarded the **{role}** role",
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=["delrole"])
    @commands.has_role("Moderators")
    async def del_roles(self, ctx, member: discord.Member, *, role: discord.Role):
        await member.remove_roles(role)
        embed = discord.Embed(
            title="**Role deleted**",
            description=f"{role} role has been revoked from {member.mention}",
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Commands(client))
