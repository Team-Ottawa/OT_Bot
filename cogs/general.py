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


def get_bag(user):
    pass


class General(commands.Cog):
    """
    General commands
    """
    def __init__(self, client):
        self.client = client

    @commands.command(help='to set your custom prefix')
    @commands.guild_only()
    async def prefix(self, ctx, *, new_prefix):
        if len(new_prefix) >= 5:
            await ctx.send("لا يمكنك وضع بادئه اكثر من 5 حرف")
            return
        db.set_prefix(ctx.author, new_prefix)
        await ctx.send("حمبي البرفكس تبعك `{}`".format(new_prefix))

    @commands.command(help='to set your custom title')
    @commands.guild_only()
    async def title(self, ctx, *, title=None):
        if ctx.author.bot:
            return
        if len(title) > 100:
            await ctx.send("تقدر تحط اكثر شي ميه حرف")
        db.set_description(ctx.author, title)
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
        # print(f'name: {member.name}')
        # print(f'bag: {" | ".join(list_bag)}')
        # print(f'Thanks: {db.get_thanks(member)}')
        # print(f'prefix: {db.get_prefix(member)}')
        # print(f'xp: {db.get_xp(member)}')
        # print(f'description: {db.get_description(member)}')
        if member.bot:
            await ctx.send("this user is bot 🙃.")
            return
        list_bag = []
        member_roles = [i.id for i in member.roles]
        if member.id in self.client.owner_ids:  # owner
            list_bag.append(str(self.client.get_emoji(826447166612570164)))

        if 804401761636319242 in member_roles:  # Helper
            list_bag.append(str(self.client.get_emoji(826449153751384084)))

        if 813508502068133888 in member_roles:  # Trusted Developer
            list_bag.append(str(self.client.get_emoji(790673460086571018)))

        if 813514566620938331 in member_roles:  # Girl
            list_bag.append(str(self.client.get_emoji(826457357176799253)))

        if 805294664960966697 in member_roles:  # Friends
            list_bag.append(str(self.client.get_emoji(654641909838381056)))

        if 805294497521074264 in member_roles:  # youtubers
            list_bag.append(str(self.client.get_emoji(826458908267905044)))

        if 663393634946908170 in member_roles:  # booster
            list_bag.append(str(self.client.get_emoji(748518646413918209)))

        if 826738623587155990 in member_roles:  # Trusted Designer
            list_bag.append(str(self.client.get_emoji(826870053554749460)))

        if list_bag == []:
            list_bag.append(str(self.client.get_emoji(826455187602145352)))
        embed = discord.Embed(
            color=member.color
        )
        embed.add_field(name='user id:', value=member.id, inline=True)
        embed.add_field(name='user name:', value=member.name, inline=True)
        embed.add_field(name='bag:', value=" | ".join(list_bag), inline=True)
        embed.add_field(name='Thanks count:', value=f'`{db.get_thanks(member)}` ✨', inline=True)
        embed.add_field(name='prefix:', value=f"`{db.get_prefix(member)}`", inline=True)
        embed.add_field(name='message count(xp):', value=f'`{db.get_xp(member)}`', inline=True)
        embed.add_field(name="description:", value=db.get_description(member))
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command(name='info')
    @commands.guild_only()
    async def info_code(self, ctx, code_id):
        data = db.get_code(code_id)
        if data is None:
            await ctx.send('حمبي هاذ الكود مش موجود, لا توجع لي راسي خذ 🥕')
            return
        await ctx.message.add_reaction('⏳')
        await ctx.message.reply(f"""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
```{data[3][:2]}\n{data[6]}\n```
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
{self.client.get_emoji(761876595770130452)} **Title** : {data[1]}
{self.client.get_emoji(761876609358757918)} **Description** : {data[2]}
{self.client.get_emoji(761876608196804609)} **shared By** : {await self.client.fetch_user(data[4])}
{self.client.get_emoji(761876614761807883)} **copyrights** : {data[5]}
{self.client.get_emoji(761876595006767104)} **language** : {data[3]}           
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
