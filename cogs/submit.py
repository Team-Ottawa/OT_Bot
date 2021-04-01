import discord
from discord.ext import commands
import asyncio
import json
import random
from discord.utils import get

with open('./config.json', 'r') as f:
    config = json.load(f)


class Sub:
    def __init__(self, client, questions: list):
        self.client = client
        self.questions = questions

    async def sub(self, ctx):
        channel = self.client.get_channel(config['submit_channel'])  # id channel
        answers = []
        embed = discord.Embed(description=ctx.author.id, color=ctx.author.color, timestamp=ctx.message.created_at)
        await ctx.author.send(embed=discord.Embed(description="لديك 3 دقائق للإجابة على كل سؤال", color=0xf7072b))
        await ctx.message.add_reaction(self.client.get_emoji(771050418498306068))
        def check(m): return m.author == ctx.author and m.author == ctx.author and str(m.channel.type) == "private"
        nam = 0
        for i in self.questions:
            nam += 1
            await ctx.author.send(embed=discord.Embed(description=i, color=0xf7072b).set_author(name=f"{nam}/{len(self.questions)}"))
            try:
                msg = await self.client.wait_for('message', timeout=180.0, check=check)
            except asyncio.TimeoutError:
                await ctx.author.send(embed=discord.Embed(
                    description="لقد تجاوزت الوقت المحدد للإرسال",
                    color=0xf7072b))
                return
            else:
                answers.append(msg.content)

        for kay, value in enumerate(self.questions):
            embed.add_field(name=f"{kay} - {value}:", value=answers[kay], inline=False)
        embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
        embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        message = await ctx.author.send(embed=discord.Embed(description="اضغط ✅ لارسال تقديمك\nاضغط ❌ للغاء تقديمك", color=discord.Color.green()))
        await message.add_reaction("✅")
        await message.add_reaction("❎")

        def check(reaction, user): return user == ctx.author and str(reaction.emoji) in ["✅", "❎"]
        try:
            reaction, user = await self.client.wait_for("reaction_add", timeout=60, check=check)

            if str(reaction.emoji) == "✅":
                await channel.send(embed=embed)
                await message.edit(embed=discord.Embed(
                    description="✅ تم ارسال تقديمك في نجاح",
                    color=discord.Color.green()
                ))
            elif str(reaction.emoji) == "❎":
                await message.edit(embed=discord.Embed(
                    description="❌ تم الغاء تقديمك",
                    color=discord.Color.red()
                ))
                return
            else:
                await message.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            await message.delete()


class Submit(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['sub'], help='submit to Helper role')
    @commands.guild_only()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def submit(self, ctx):
        random_questions = [
            "ما الفرق بين Node.js و JavaScript؟",
            "اذكر نوعين من قواعد البيانات في البرمجه؟",
            "ما الذي تحتاجه لإنشاء موقع ويب كامل؟",
            "أذكر نوعين من انواع البيانات في البرمجة؟",
            "ما هو المتغير في لغات البرمجه؟",
            "ما هو تعريف العدد في لغات البرمجة؟",
        ]
        submit = Sub(self.client, [
                    '1️⃣ | اكتب اسمك الآن: ',
                    '2️⃣ | اكتب عمرك الآن: ',
                    '3️⃣ | اكتب لغتك البرمجيه الآن: ',
                    '4️⃣ | أرسل لنا مشروعًا أو روبوتًا صممته بنفسك (إذا كنت قد أخذت الروبوت من شخص ما ، فسيتم رفضك): ',
                    '5️⃣ | {}: '.format(random.choice(random_questions)),
                    '6️⃣ | قبل استكمال الطلب برجاء قراءة القوانين من هنا <#781902561333870623> ',
                ])
        await submit.sub(ctx)


def setup(client):
    client.add_cog(Submit(client))
