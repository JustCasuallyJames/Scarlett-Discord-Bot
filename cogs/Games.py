import random

import discord
from discord.ext import commands


class Games(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def coinflip(self, ctx, choice: str, *, gamble):
        member = ctx.message.author
        guild_id = ctx.message.guild.id
        cog = self.client.get_cog("Money")
        bank = await cog.get_coins(member.id, guild_id)
        all = "ALL"
        HEAD_CHOICES = ("Heads", "heads", "h", "hd", "head")
        TAIL_CHOICES = ("Tails", "tails", "t", "tl", "tail")
        if gamble in f"{all.lower()}":
            if bank == 0:
                await ctx.send("You have insufficient funds.")
            else:
                winning_answers = random.choice([HEAD_CHOICES, TAIL_CHOICES])
                if choice.lower() in winning_answers:  # this is a checking if your choice is within the tuple, winning_answers
                    await cog.add_coins(member.id, guild_id, bank)
                    await ctx.send(f"Flip: {winning_answers[0]}. You won {bank} coins!")
                else:
                    await cog.sub_coins(member.id, guild_id, bank)
                    await ctx.send(f"Flip: {winning_answers[0]}. You lost {bank} coins!")
        else:
            if int(gamble) > bank or int(gamble) == 0:
                await ctx.send("You have insufficient funds.")
                return
            else:
                winning_answers = random.choice([HEAD_CHOICES, TAIL_CHOICES])
                # 1 is heads 0 is tails
                if choice.lower() in winning_answers:  # this is a checking if your choice is within the tuple, winning_answers
                    await cog.add_coins(member.id, guild_id, int(gamble))
                    await ctx.send(f"Flip: {winning_answers[0]}. You won {int(gamble)} coins!")
                else:
                    await cog.sub_coins(member.id, guild_id, int(gamble))
                    await ctx.send(f"Flip: {winning_answers[0]}. You lost {int(gamble)} coins!")






    # for the countdown, maybe can do the reaction countdown. ie 10 9 8 7 6 after every second then delete
    # the message afterwards?
    # def chicken_fight_one(self, name1, name2):
    #     possible_choices_name1 = [f"{name1} pecks {name2}",
    #                               f"{name1} flies and does a flying roundhouse kick on {name2}",
    #                               f"{name1} catches {name2} off guard and proceeds to do the primary lotus on {name2}\n",
    #                               f"{name1} grabs onto {name2} leg and throws up against the ring railing",
    #                               f"",
    #                               f"",
    #                               f"",
    #                               ]
    #     return f"""
    #     {name1}, the chicken, and {name2}, the chicken enter the ring.\n
    #     {name1} swoops in and knocks {name2} off their legs. {name2} falls but manages to\n
    #     land a peck in the eye of {name1}. {name1} is currently blinded and can't see anything.\n
    #     {name2} takes this opportunity to attack to bring {name1} down. {name2} keeps {name1} pinned\n
    #     down with {name1} not being able to escape. 10 seconds pass and {name1} taps out!
    #     {name2} wins the cockfight!
    #     """

    # @commands.command(aliases=["chickenfight"])
    # async def chicken_fight(self):
    #     fight_scene=


def setup(client):
    client.add_cog(Games(client))
