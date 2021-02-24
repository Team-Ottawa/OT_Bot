import discord
from discord.ext import commands
import time


class Verified(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="verified", aliases=["verify", "تحقق"])
    async def verified_command(self, ctx):
        if ctx.channel.id != 813520464872734740:
            return
        await ctx.author.add_roles(discord.utils.get(ctx.author.guild.roles, name="Verified"))
        await ctx.author.send(embed=discord.Embed(
            description="Your account has been verified and give role **@Verified**",
            color=discord.Colour.red()
        ))

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.channel.id != 813520464872734740:
            return
        if ctx.author.id == 739232997232082944:
            return
        if ctx.author.bot:
            return
        time.sleep(0.2)
        await ctx.delete()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def rm(self, ctx):
        embed = discord.Embed(
            description="""
**#العربيه :flag_sa:**
**يمكنك طلب اكواد عن طريقه اتباع التالي:**
======================
**اسم بوتك: **
**عنوان الكود: **
**وصف الكود: **
======================

ملاحظه: الاجابه على طلبك ليس مؤكد.


** You can request codes through the following: **
======================
** Your Bot Name: **
** Code Title: **
** Code description: **
======================

Note: The answer to your request is not certain.
""",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ro(self, ctx):
        embed = discord.Embed(
            description="""
**#العربيه :flag_sa:**
**لم يتم التحقق منك حاليا في الخادم.**
هذا يعني أنه لا يمكنك الوصول إلى قنوات أخرى والتحدث مع الناس.

لمعرفة كيفية الحصول على رتبه <@&813508149167652866> ، يرجى الانتقال إلى <#813541018107772938> .

**#English :flag_us:**
** You are currently not verified on the server. **
This means that you cannot reach other channels and talk to people.

To find out how to get <@&813508149167652866> role, please go to <#813541018107772938>.
""",
            color=discord.Color.red()
        )
        # await ctx.send(embed=embed)
        await ctx.send("[ @everyone ]", embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def rl(self, ctx):
        embed = discord.Embed(
            description="""
**#العربيه :flag_sa:**
**لم يتم التحقق منك حاليا في الخادم.**
للتحقق استعمل امر `!تحقق`, سوف تحصل على رتبه <@&813508149167652866> .

**#English :flag_us:**
** You are currently not verified on the server. **

To verify use the `!verify` command, you will get the <@&813508149167652866> role.
"""
        )
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Verified(client))
