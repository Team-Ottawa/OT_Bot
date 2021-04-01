import discord
from discord.ext import commands
import asyncio
import json
import db
import random

with open('./config.json', 'r') as f:
    config = json.load(f)


def get_code_id():
    date = "qwertyuiopasdfghjklzxcvbnm_-1234567890"
    data_ = db.cr.execute("SELECT * FROM vip").fetchall()
    da = [i for i in data_]
    id = ""

    def gen_id(id):
        while len(id) != 10:
            value = random.choice(date)
            id += value
        return id
    if gen_id in da:
        gen_id(id)
    return gen_id(id)


class PostCode(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.cooldown(1, 300, commands.BucketType.user)
    @commands.has_any_role(config['coder_role_name'])
    async def js(self, ctx):
        share = Share(self.client, 781903206762020904, "javascript", [
            'Write the code now without putting tags:',
            'Write the copyright:',
            'Write the code title:',
            'Write the code description:',
            'Confirm Code Share (Yes / No):'])
        await share.share(ctx, mention=True)

    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.cooldown(1, 300, commands.BucketType.user)
    @commands.has_any_role(config['coder_role_name'])
    async def py(self, ctx):
        share = Share(self.client, 826883707465105408, "python", [
            'Write the code now without putting tags:',
            'Write the copyright:',
            'Write the code title:',
            'Write the code description:',
            'Confirm Code Share (Yes / No):'])
        await share.share(ctx, mention=True)

    @commands.command(help='post your code')
    @commands.guild_only()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def post(self, ctx):
        share = Share(self.client, 826883707465105408, "javascript", [
            'Write the code now without putting tags:',
            'Write the copyright:',
            'Write the code title:',
            'Write the code description:',
            'Confirm Code Share (Yes / No):'])
        await share.share(ctx, mention=False)


def setup(client):
    client.add_cog(PostCode(client))


class Share:
    def __init__(self, client, channel: int, type: str, questions: list):
        self.client = client
        self.channel = channel
        self.questions = questions
        self.type = type

    async def share(self, ctx, mention=False):
        channels = [811002423303995442, 813533585646551041, 810949112433213450, 813851049722511390]
        if ctx.channel.id not in channels:
            return
        if ctx.author.bot:
            return
        channel = self.client.get_channel(self.channel)  # id channel
        answers = []
        await ctx.author.send(embed=discord.Embed(
            description="You have 3 minutes to answer each question",
            color=0xf7072b
        ))
        await ctx.message.add_reaction('✅')

        def check(m):
            return m.author == ctx.author and m.author == ctx.author and str(m.channel.type) == "private"

        for i in self.questions:
            await ctx.author.send(embed=discord.Embed(
                description=i,
                color=0xf7072b))
            try:
                msg = await self.client.wait_for('message', timeout=180.0, check=check)
            except asyncio.TimeoutError:
                await ctx.author.send(embed=discord.Embed(
                    description='You have exceeded the specified time',
                    color=0xf7072b))
                return
            else:
                answers.append(msg.content)
        if answers[4].lower() == 'yes':
            await ctx.author.send(embed=discord.Embed(
                description='Your code has been shared with everyone',
                color=0xf7072b))
            embed = discord.Embed(description=f'''
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
```{self.type[:2]}\n{answers[0]}\n```
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
{self.client.get_emoji(761876595770130452)} **codes** : {answers[2]}
{self.client.get_emoji(761876609358757918)} **Description** : {answers[3]}
{self.client.get_emoji(761876608196804609)} **shared By** : {ctx.author.mention}
{self.client.get_emoji(761876614761807883)} **copyrights** : {answers[1]}
{self.client.get_emoji(761876595006767104)} **language** : {self.type}
    ''')
            if mention:
                await channel.send(ctx.guild.get_role(813514248142717011).mention, embed=embed)
                db.cr.execute("INSERT OR IGNORE INTO codes(code_id, coder_id, code, type_code) VALUES(?, ?, ?, ?)", (
                    get_code_id(), ctx.author.id, answers[0], self.type))
                db.db.commit()
                return
            await channel.send(embed=embed)
            return
        elif answers[4].lower() == 'no':
            await ctx.author.send(embed=discord.Embed(
                description='The code has been unshared',
                color=0xf7072b))
            return
        else:
            await ctx.author.send(embed=discord.Embed(
                description="❌ It seems that you have chosen the wrong answer. You can reapply again after 5 minutes",
                color=0xf7072b
            ))
            return
