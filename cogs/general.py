import discord
from discord.ext import commands
import time
import db
import random

replay = {
    "صقر": "يا عمر صقر",
    "حازم": "اسطوره البايثون عطه لكزز",
    "بترولي": "يعني يوسف يعني طيران يعني حبيبي والله",
    "يوسف": "يعني بترولي يعني طيران يعني حبيبي والله",
    "-": "**Welcome To Server Ottawa Please Check <#781902561333870623> <:b9c0dcde98313119:762315185670062121> !**",
    ".": "**Welcome To Server Ottawa Please Check <#781902561333870623> <:b9c0dcde98313119:762315185670062121> !**",
    "السلام عليكم": "وعليكم السلام ورحمة الله وبركاته، نورت السيرفر",
    "السلام عليكم ورحمة الله وبركاته": "وعليكم السلام ورحمة الله وبركاته، نورت السيرفر",
    "سلام عليكم ورحمة الله وبركاته": "سلام عليكم ورحمة الله وبركاته",
    "سلام عليكم": "وعليكم السلام ورحمة الله وبركاته، نورت السيرفر",
    "@everyone": "<a:gh:811299417151897622>",
    "@here": "<a:gh:811299417151897622>"
}


def get_bag(client, member: discord.Member) -> list:
    list_bag = []
    member_roles = [i.id for i in member.roles]
    if member.id in client.owner_ids:  # owner
        list_bag.append(str(client.get_emoji(826447166612570164)))

    if 804401761636319242 in member_roles:  # Helper
        list_bag.append(str(client.get_emoji(826449153751384084)))

    if 813508502068133888 in member_roles:  # Trusted Developer
        list_bag.append(str(client.get_emoji(790673460086571018)))

    if 813514566620938331 in member_roles:  # Girl
        list_bag.append(str(client.get_emoji(826457357176799253)))

    if 805294664960966697 in member_roles:  # Friends
        list_bag.append(str(client.get_emoji(654641909838381056)))

    if 805294497521074264 in member_roles:  # youtubers
        list_bag.append(str(client.get_emoji(826458908267905044)))

    if 663393634946908170 in member_roles:  # booster
        list_bag.append(str(client.get_emoji(748518646413918209)))

    if 826738623587155990 in member_roles:  # Trusted Designer
        list_bag.append(str(client.get_emoji(826870053554749460)))

    if list_bag == []:
        list_bag.append(str(client.get_emoji(826455187602145352)))

    return list_bag


class General(commands.Cog):
    """
    General commands
    """
    def __init__(self, client):
        self.client = client

    @commands.command(help='to set your custom title')
    @commands.guild_only()
    async def title(self, ctx, *, title=None):
        if ctx.author.bot:
            return
        if len(title) > 100:
            await ctx.send("تقدر تحط اكثر شي ميه حرف")
            return
        x = db.DatabaseUsers(self.client, ctx.author.id)
        x.update_where("description", title)
        await ctx.message.add_reaction(self.client.get_emoji(771050418498306068))

    @commands.command(invoke_without_command=True, hidden=True)
    @commands.guild_only()
    async def ping(self, ctx):
        before = time.monotonic()
        msg = await ctx.send("pong!")
        ping = (time.monotonic() - before) * 1000
        await msg.edit(content="```c\nTime taken: {}ms\nDiscord API: {}ms```".format(int(ping), round(self.client.latency * 1000)))

    @commands.command(help='show the info users')
    @commands.guild_only()
    async def profile(self, ctx, member: discord.Member = None):
        member = member if member else ctx.author
        if member.bot:
            await ctx.send("this user is bot 🙃.")
            return
        x = db.DatabaseUsers(self.client, member.id)
        embed = discord.Embed(
            color=member.color
        )
        embed.add_field(name='user id:', value=member.id, inline=True)
        embed.add_field(name='user name:', value=member.name, inline=True)
        embed.add_field(name='bag:', value=" | ".join(get_bag(self.client, member)), inline=True)
        embed.add_field(name='Thanks count:', value=f'`{x.info.get("thanks")}` ✨', inline=True)
        embed.add_field(name='message count(xp):', value=f'`{x.info.get("xp")}`', inline=True)
        embed.add_field(name="description:", value=x.info.get("description"))
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command(name='info', help="Show info code by id")
    @commands.guild_only()
    async def info_code(self, ctx, code_id):
        x = db.DatabaseCodes(self.client, code_id)
        data = x.info
        if data is None:
            await ctx.send('حمبي هاذ الكود مش موجود, لا توجع لي راسي خذ 🥕')
            return

        await ctx.message.add_reaction('⏳')
        await ctx.message.reply(f"""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
```{data.get("type")[:2]}\n{data.get("code")}\n```
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
{self.client.get_emoji(761876595770130452)} **Title** : {data.get("title")}
{self.client.get_emoji(761876609358757918)} **Description** : {data.get("description")}
{self.client.get_emoji(761876608196804609)} **shared By** : {await self.client.fetch_user(data.get("author_id"))}
{self.client.get_emoji(761876614761807883)} **copyrights** : {data.get("copyrights")}
{self.client.get_emoji(761876595006767104)} **language** : {data.get("type")}
⏳ **Add At:** {data.get("data")}
🔗 **Pastebin:** <{data.get("link")}>
""", allowed_mentions=discord.AllowedMentions.none())

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.guild is None:
            return
        if ctx.author.bot:
            return
        if ctx.content in replay:
            await ctx.reply(content=replay[ctx.content])


def setup(client):
    client.add_cog(General(client))
