import discord
from discord.ext import commands
import time
import config
import db
from discord_ui import SlashOption
from discord_ui.cogs import slash_cog


replay = {
    "صقر": "يا عمر صقر",
    "حازم": "اسطوره البايثون عطه لكزز",
    "بترولي": "يعني يوسف يعني طيران يعني حبيبي والله",
    "يوسف": "يعني بترولي يعني طيران يعني حبيبي والله",
    "-": "**Welcome To Server Ottawa Please Check <#843868609864400938> <:b9c0dcde98313119:762315185670062121> !**",
    ".": "**Welcome To Server Ottawa Please Check <#843868609864400938> <:b9c0dcde98313119:762315185670062121> !**",
    "السلام عليكم": "وعليكم السلام ورحمة الله وبركاته، نورت السيرفر",
    "السلام عليكم ورحمة الله وبركاته": "وعليكم السلام ورحمة الله وبركاته، نورت السيرفر",
    "سلام عليكم ورحمة الله وبركاته": "سلام عليكم ورحمة الله وبركاته",
    "سلام عليكم": "وعليكم السلام ورحمة الله وبركاته، نورت السيرفر",
    "@everyone": "<a:gh:811299417151897622>",
    "@here": "<a:gh:811299417151897622>"
}


class General(commands.Cog):
    """
    General commands
    """
    def __init__(self, client):
        self.client = client

    @slash_cog(
        name="ping",
        guild_ids=[config.guild_id],
    )
    async def ping(self, ctx):
        before = time.monotonic()
        msg = await ctx.respond("pong!")
        ping = (time.monotonic() - before) * 1000
        await msg.edit(content="```c\nTime taken: {}ms\nDiscord API: {}ms```".format(int(ping), round(self.client.latency * 1000)))

    @slash_cog(
        name="title",
        description="تغير وصفك",
        guild_ids=[config.guild_id],
        options=[
            SlashOption(
                str,
                name="title",
                description="to set your custom title",
                required=True,
            )
        ]
    )
    async def title(self, ctx, title):
        if ctx.author.bot:
            return
        if len(title) > 100:
            await ctx.send("تقدر تحط اكثر شي ميه حرف")
            return
        x = db.DatabaseUsers(self.client, ctx.author.id)
        x.update_where("description", title)
        await ctx.respond("ابشر به تم من الشنب")

    @slash_cog(
        name="profile",
        description="show the info users",
        guild_ids=[config.guild_id]
    )
    async def profile(self, ctx, member: discord.Member = None):
        member = member if member else ctx.author
        if member.bot:
            await ctx.respond("this user is bot 🙃.")
            return
        x = db.DatabaseUsers(self.client, member.id)
        embed = discord.Embed(
            color=member.color
        )
        embed.add_field(name='user id:', value=member.id, inline=True)
        embed.add_field(name='user name:', value=member.name, inline=True)
        embed.add_field(name='Thanks count:', value=f'`{x.info.get("thanks")}` ✨', inline=True)
        embed.add_field(name='message count(xp):', value=f'`{x.info.get("xp")}`', inline=True)
        embed.add_field(name="description:", value=x.info.get("description"))
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)
        await ctx.respond(embed=embed)

    @slash_cog(
        name="info",
        description="Show info code by id",
        guild_ids=[config.guild_id],
    )
    async def info_code(self, ctx, code_id: str):
        x = db.DatabaseCodes(self.client, code_id)
        data = x.info
        if data is None:
            await ctx.respond('حمبي هاذ الكود مش موجود, لا توجع لي راسي خذ 🥕')
            return
        other = f"""
{self.client.get_emoji(861366683602911232)} **Title** : {data.get("title")}
{self.client.get_emoji(861366683381923850)} **Description** : {data.get("description")}
{self.client.get_emoji(861366683426619402)} **shared By** : {await self.client.fetch_user(data.get("author_id"))}
{self.client.get_emoji(861366683057651722)} **copyrights** : {data.get("copyrights")}
{self.client.get_emoji(861366681762267157)} **language** : {data.get("type")}
⏳ **Add At:** {data.get("data")}
🔗 **Pastebin:** <{data.get("link")}>
        """
        try:
            await ctx.respond(f"""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
```{data.get("type")}\n{data.get("code")}\n```
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
{other}
""", allowed_mentions=discord.AllowedMentions.none())
        except discord.errors.HTTPException:
            await ctx.respond(f"""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
{data.get("link")}
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
{other}
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
