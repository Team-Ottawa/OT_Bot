import discord
from discord.ext import commands
import config
import db
import random
import string
from discord_ui.cogs import slash_cog
from discord_ui import SlashOption, Button, ButtonStyles
from discord import ui
from asyncio import TimeoutError
from datetime import datetime


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class PostCode(commands.Cog):
    def __init__(self, client):
        self.client = client

    @slash_cog(
        name="post",
        description="post your code",
        guild_ids=[config.guild_id],
        options=[
            SlashOption(
                str,
                name="type",
                description="select type code",
                required=True,
                choices=[
                    {
                        "name": "JavaScript",
                        "value": "javascript",
                    },
                    {
                        "name": "Python",
                        "value": "python",
                    },
                ]
            )
        ]
    )
    async def post(self, ctx, type):
        await ctx.respond("check DM", hidden=True)
        channel_id = 870796766746906654  # logs code channel id
        mention = True
        if not config.coder_role_id in [i.id for i in ctx.author.roles]:
            mention = False
            channel_id = 861306905061621771  # member code channel id
        share = Share(self.client, channel_id, type)
        await share.share(ctx, mention=mention)


def setup(client):
    client.add_cog(PostCode(client))


class Share:
    def __init__(self, client, channel: int, type: str):
        self.client = client
        self.channel = channel
        self.questions = [
            ':one: |  \`\`\` اكتب الكود بدون علامات',
            ':two: | اكتب حقوق مالك الكود:',
            ':three: | اكتب عنوان الكود:',
            ':four: | اكتب وصف مفصل عن الكود:',
        ]
        self.type = type

    async def share(self, ctx, mention=False):
        channel = self.client.get_channel(self.channel)  # id channel
        answers = []
        await ctx.author.send(embed=discord.Embed(
            description="معاك ثلاث دقايق اذا ما تجاوب بسحب عليك",
            color=0xf7072b
        ))

        def check(m):
            return m.author == ctx.author and m.author == ctx.author and str(m.channel.type) == "private"

        for i in self.questions:
            await ctx.author.send(embed=discord.Embed(
                description=i,
                color=0xf7072b))
            try:
                msg = await self.client.wait_for('message', timeout=180.0, check=check)
            except TimeoutError:
                await ctx.author.send(embed=discord.Embed(
                    description='للاسف بسحب عليك',
                    color=0xf7072b))
                return
            else:
                answers.append(msg.content)
        yes = Button(
            label="Yes",
            color="green",
            emoji="✅",
            custom_id="true"
        )
        no = Button(
            label="No",
            color="red",
            emoji="❌",
            custom_id="false"
        )
        embed = discord.Embed(
            description=":five: | هل انت موافق على نشر الكود",
            color=0xf7072b
        )
        yes_or_no = await ctx.author.send(embed=embed, components=[yes, no])

        try:
            res = await yes_or_no.wait_for("button", self.client, timeout=15)
            await res.respond(ninja_mode=True)
            yes.disabled = True
            no.disabled = True
            await yes_or_no.edit(components=[yes, no])
            if res.custom_id == "true":
                id = id_generator()
                x = db.DatabaseCodes(self.client, id)
                x.insert(answers[2], answers[3], self.type, ctx.author.id, answers[1], answers[0])
                data = x.info
                content = f"""
{self.client.get_emoji(861366683602911232)} **Title** : {data.get("title")}
{self.client.get_emoji(861366683381923850)} **Description** : {data.get("description")}
{self.client.get_emoji(861366683426619402)} **shared By** : {await self.client.fetch_user(data.get("author_id"))}
{self.client.get_emoji(861366683057651722)} **copyrights** : {data.get("copyrights")}
{self.client.get_emoji(861366681762267157)} **language** : {data.get("type")}
⏳ **Add At:** {datetime.fromtimestamp(data.get("data")).strftime("%m/%d/%Y, %H:%M:%S")}
**[Pastebin]({data.get("link")}) | [Discord](https://discord.gg/ottawa) | [Programming](https://discord.com/channels/@me/{data.get("author_id")})**
                """
                await ctx.author.send(embed=discord.Embed(
                    description=f'Your code id: {id}, pls wait to accept.',
                    color=0xf7072b))

                embed = discord.Embed(
                    title=f'code id: {data.get("_id")}',
                    description=f"""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
```{data.get("type")}\n{data.get("code")}\n```
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
{content}""")
                if len(embed.description) >= 2000:
                    embed.description = f"""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
{data.get("link")}
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
{content}"""
                if mention is False:
                    await channel.send(f"code DI: {id}", embed=embed)
                    return

                await channel.send(f"{ctx.guild.get_role(843871660625231902).mention} | {id}", embed=embed)
                return
            await ctx.author.send(embed=discord.Embed(description="تم الغاء الامر", color=0xf7072b))
        except TimeoutError:
            yes.disabled = True
            no.disabled = True
            return await yes_or_no.edit(components=[yes, no])

