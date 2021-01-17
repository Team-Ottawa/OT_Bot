import discord
from discord.ext import commands
import asyncio
import json
import random
from discord.utils import get

with open('./config.json', 'r') as f:
    config = json.load(f)


class submit(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['sub'])
    @commands.guild_only()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def submit(self, ctx):
        channel = self.client.get_channel(config['submit_channel'])  # id channel
        random_questions = [
            "What is the difference between Node.js and JavaScript?",
            "List two types of database?",
            "What do you need to create a complete website?",
            "Mention two general data types in programming?",
            "What is the variable?",
            "What is an integer in programming languages?"
        ]
        ran = random.choice(random_questions)

        questions_1 = [
            '1️⃣ | Write your name now:',
            '2️⃣ | Write your age now:',
            '3️⃣ | Write your name language now:',
            '4️⃣ | Send us a project or no bot that you designed yourself (if you have taken the bot from someone, you will be rejected):',
            '5️⃣ | {}:'.format(ran),
            '6️⃣ | Before completing the application, please read the laws from here <#781902561333870623>',
            '7️⃣ | Your submission has been completed. If you agree to send your submission or not (yes / no)']
        answers = []

        await ctx.author.send(
            embed=discord.Embed(
                description="You have 3 minutes to answer each question",
                color=0xf7072b))
        await ctx.message.add_reaction('✅')

        def check(m):
            return m.author == ctx.author and m.author == ctx.author
        for i in questions_1:
            await ctx.author.send(embed=discord.Embed(
                    description=i,
                    color=0xf7072b))
            try:
                msg = await self.client.wait_for('message', timeout=180.0, check=check)
            except asyncio.TimeoutError:
                await ctx.author.send(embed=discord.Embed(
                    description='You have exceeded the time specified for submission',
                    color=0xf7072b))
                return
            else:
                answers.append(msg.content)

        if answers[6] == 'yes' or answers[6] == 'Yes' or answers[6] == 'YEs' or answers[6] == 'YES':
            await ctx.author.send(embed=discord.Embed(
                description="✅ Your review has been submitted. Please wait for a response from Mod\nYou should wait 1h/24h max",
                color=0xf7072b))

            embed = discord.Embed(
                description=ctx.author.id,
                color=ctx.author.color,
                timestamp=ctx.message.created_at)
            embed.add_field(
                name=questions_1[0],
                value=answers[0],
                inline=False)
            embed.add_field(
                name=questions_1[1],
                value=answers[1],
                inline=False)
            embed.add_field(
                name=questions_1[2],
                value=answers[2],
                inline=False)
            embed.add_field(
                name=questions_1[3],
                value=answers[3],
                inline=False)
            embed.add_field(
                name=questions_1[4],
                value=answers[4],
                inline=False)
            embed.add_field(
                name="6️⃣ | Before completing the application, please read the laws from here #Rulse",
                value=answers[5],
                inline=False)
            embed.add_field(
                name=questions_1[6],
                value=answers[6],
                inline=False)

            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=ctx.guild.icon_url)

            await channel.send(embed=embed)
            return
        elif answers[6] == 'no' or answers[6] == 'No' or answers[6] == 'NO':
            await ctx.author.send(
                embed=discord.Embed(
                    description="❌ Your submission has been canceled",
                    color=0xf7072b))
            return
        else:
            await ctx.author.send(embed=discord.Embed(
                description="❌ It seems that you have chosen the wrong answer. You can reapply again after 24h",
                color=0xf7072b
            ))
            return
        # await ctx.message.add_reaction('❌')

    @submit.error
    async def submit_error(self, ctx, error):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(embed=discord.Embed(
                description="❌ Please open your DM before applying and reapply again after 24h",
                color=0xf7072b
            ))
        if isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            await ctx.send(embed=discord.Embed(
                description="❌ It seems that you have chosen the wrong answer. You can reapply again after {}".format("%d hour, %02d minutes, %02d seconds" % (h, m, s)),
                color=0xf7072b
            ))
        else:
            print(error)


def setup(client):
    client.add_cog(submit(client))
