import discord
from discord.ext import commands

import json
import sys
import traceback



class Events(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is ready........")

    @commands.Cog.listener()
    async def on_message(self, message):
        with open('data/prefixes.json', 'r') as f:
            prefixes = json.load(f)
        if message.content.startswith('mc'):
            await message.channel.send('No fuck you')
        if message.content.startswith('pepega'):
            await message.channel.send("Yes we know you're pepega..")
        if message.content.startswith('prefix'):
            await message.channel.send(f"\nThe current prefix is: {prefixes[str(message.author.guild.id)]}")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open('data/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(guild.id)] = '.'

        with open('data/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open('data/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes.pop(str(guild.id))

        with open('data/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # This doesn't show the bot joining because it can't consider itself joining
        print(f'{member} has joined the server.')
        role = discord.utils.get(member.guild.roles, name='Casual Crew')
        await member.add_roles(role)
        # sends the user a DM
        await member.send(f"You've been awarded the **{role}** role")
        channel = member.guild.get_channel(661163292311552040)
        embed = discord.Embed(
            title="**Welcome**",
            description=f"{member.mention} just joined our server!",
            colour=discord.Colour.green()
        )
        embed.set_thumbnail(
            url=f"{member.avatar_url}")
        embed.set_footer(text=f"ID: {member.id}")
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} has left the server.')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # This would give an error message if it hasn't passed all the necessary inputs
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send("You're missing an input")
        # Happens when a member without the required role tries to type a command.
        if isinstance(error, commands.MissingRole):
            return await ctx.send(f"You don't have the **{error.missing_role}** role that is required to do this.")
        # Happens when a member puts in the wrong argument into the command
        if isinstance(error, commands.BadArgument):
            return await ctx.send(f"{error}")
        if isinstance(error, commands.UnexpectedQuoteError):
            return await ctx.send('There is a random quotation mark.')
        if isinstance(error, commands.InvalidEndOfQuotedStringError):
            return await ctx.send('Word(s) are being written after two "".')
        if isinstance(error, commands.ExpectedClosingQuoteError):
            return await ctx.send('There is no closing quote.')
        if isinstance(error, commands.CommandNotFound):
            return
        print(f"Ignoring exception in command {ctx.command}", file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(client):
    client.add_cog(Events(client))
