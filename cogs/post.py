import discord
from discord.ext import commands
import asyncio
import config
import db
import random
import string
from discord.utils import get
from datetime import datetime
import datetime


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class PostCode(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help='post your code')
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def post(self, ctx):
        if ctx.author.bot:
            return
        questions = [
            ':one: |  \`\`\` اكتب الكود بدون علامات',
            ':two: | اكتب حقوق مالك الكود:',
            ':three: | اكتب عنوان الكود:',
            ':four: | اكتب وصف مفصل عن الكود:',
            ':five: | هل انت موافق على نشر الكود (Yes or No):'
        ]
        x = 3
        if config.coder_role_id in [i.id for i in ctx.author.roles]:
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel and m.content in ['1', '2', '3']

            embed = discord.Embed(
                title='اختار نوع نشر الكود حسب الرقم:',
                color=0xFF0000,
                description=
                "**[ 1 ]** : JavaScript code post\n**[ 2 ]** : Python code post\n**[ 3 ]** : Normal post"
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
            embed.set_thumbnail(url=ctx.guild.icon_url)
            m = await ctx.send(embed=embed)
            try:
                message = await self.client.wait_for("message", timeout=180.0, check=check)
            except asyncio.TimeoutError:
                await m.delete()
                return
            x = int(message.content)
        if x == 1:
            share = Share(self.client, 870796766746906654, "javascript", questions)
            await share.share(ctx, mention=True)
        elif x == 2:
            share = Share(self.client, 870796766746906654, "python", questions)
            await share.share(ctx, mention=True)
        elif x == 3:
            share = Share(self.client, 861306905061621771, "javascript", questions)
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
            id = id_generator()
            x = db.DatabaseCodes(self.client, id)
            x.insert(answers[2], answers[3], self.type, ctx.author.id, answers[1], answers[0])
            data = x.info
            await ctx.author.send(embed=discord.Embed(
                description=f'Your code id: {id}, pls wait to accept.',
                color=0xf7072b))

            embed = discord.Embed(
                title=f'code id: {data.get("_id")}',
                description=f"""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
```{data.get("type")[:2]}\n{data.get("code")}\n```
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
{self.client.get_emoji(761876595770130452)} **Title** : {data.get("title")}
{self.client.get_emoji(761876609358757918)} **Description** : {data.get("description")}
{self.client.get_emoji(761876608196804609)} **shared By** : {await self.client.fetch_user(data.get("author_id"))}
{self.client.get_emoji(761876614761807883)} **copyrights** : {data.get("copyrights")}
{self.client.get_emoji(761876595006767104)} **language** : {data.get("type")}
⏳ **Add At:** {data.get("data")}
**[Pastebin]({data.get("link")}) | [Discord](https://discord.gg/Q5pd2veeH7) | [Programming](https://discord.com/channels/@me/{data.get("author_id")})**
            """)
            if mention is False:
                await channel.send(f"code DI: {id}", embed=embed)
                return
            await channel.send(f"{ctx.guild.get_role(843871660625231902).mention} | {id}", embed=embed)
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
