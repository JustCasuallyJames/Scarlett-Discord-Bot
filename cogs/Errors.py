import discord
from discord.ext import commands

import sys
import traceback

from time import gmtime
from time import strftime

class Errors(commands.Cog):

    def __init__(self, client):
        self.client = client

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
            return await ctx.send(f"{error}")
        if isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            return await ctx.send(f"Currently on cooldown. Please wait **{int(h)} hours {int(m)} minutes {int(s)} seconds**")

        print(f"Ignoring exception in command {ctx.command}", file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(client):
    client.add_cog(Errors(client))
