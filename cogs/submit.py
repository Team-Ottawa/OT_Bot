import discord
from discord.ext import commands
import asyncio
import json
import random
from discord.utils import get

with open('./config.json', 'r') as f:
    config = json.load(f)


class Submit(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['sub'])
    @commands.guild_only()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def submit(self, ctx):
        embed = discord.Embed(
            description="**Choose the type of rank you want?**\n:black_circle: : Admin\n:yellow_circle: : coder",
            color=discord.Color.red()
        )
        message = await ctx.author.send(embed=embed)

        await ctx.message.add_reaction('✅')

        await message.add_reaction("⚫")
        await message.add_reaction("🟡")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["⚫", "🟡"]

        try:
            reaction, user = await self.client.wait_for("reaction_add", timeout=60, check=check)

            if str(reaction.emoji) == "⚫":
                embed = discord.Embed(
                    description="**enter your language?**\n:black_circle: : English Language\n:yellow_circle: : لغه عربيه",
                    color=discord.Color.red()
                )
                message = await ctx.author.send(embed=embed)

                await ctx.message.add_reaction('✅')
                lang = "en"

                await message.add_reaction("⚫")
                await message.add_reaction("🟡")

                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in ["⚫", "🟡"]

                try:
                    reaction, user = await self.client.wait_for("reaction_add", timeout=60, check=check)

                    if str(reaction.emoji) == "⚫":
                        lang = "en"
                    elif str(reaction.emoji) == "🟡":
                        lang = "ar"
                    else:
                        await message.remove_reaction(reaction, user)

                except asyncio.TimeoutError:
                    await message.delete()
                channel = self.client.get_channel(config['submit_channel'])  # id channel
                en_questions = [
                    '1️⃣ | Write your name now:',
                    '2️⃣ | Write your age now:',
                    '3️⃣ | Write down when you interacted on the server:',
                    '4️⃣ | Have you ever been an administrator in a server?:',
                    '5️⃣ | Before completing the application, please read the laws from here <#781902561333870623>',
                ]
                ar_questions = [
                    '1️⃣ | اكتب اسمك الآن: ',
                    '2️⃣ | اكتب عمرك الآن: ',
                    '3️⃣ | اكتب وقت تفاعلك في السيرفر الآن: ',
                    '4️⃣ | هل سبق لك و كنت اداري في احدى السيرفرات: ',
                    '6️⃣ | قبل استكمال الطلب برجاء قراءة القوانين من هنا <#781902561333870623> ',
                ]
                answers = []
                embed = discord.Embed(
                    description=ctx.author.id,
                    color=ctx.author.color,
                    timestamp=ctx.message.created_at
                )
                m = "You have 3 minutes to answer each question"
                if lang == "ar":
                    m = "لديك 3 دقائق للإجابة على كل سؤال"
                await ctx.author.send(
                    embed=discord.Embed(
                        description=m,
                        color=0xf7072b))

                def check(m):
                    return m.author == ctx.author and m.author == ctx.author and str(m.channel.type) == "private"

                nam = 0
                if lang == "ar":
                    en_questions = ar_questions
                for i in en_questions:
                    nam += 1
                    await ctx.author.send(embed=discord.Embed(
                        description=i,
                        color=0xf7072b).set_author(name=f"{nam}/{len(en_questions)}"))
                    try:
                        msg = await self.client.wait_for('message', timeout=180.0, check=check)
                    except asyncio.TimeoutError:
                        m = 'You have exceeded the time specified for submit'
                        if lang == "ar":
                            m = "لقد تجاوزت الوقت المحدد للإرسال"
                        await ctx.author.send(embed=discord.Embed(
                            description=m,
                            color=0xf7072b))
                        return
                    else:
                        answers.append(msg.content)

                for kay, value in enumerate(en_questions):
                    embed.add_field(
                        name=f"{kay} - {value}:",
                        value=answers[kay],
                        inline=False
                    )
                embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.set_thumbnail(url=ctx.guild.icon_url)
                m = "rect ✅ to send your submit\nrect ❎ to cancel yot submit"
                if lang == "ar":
                    m = "اضغط ✅ لارسال تقديمك\nاضغط ❌ للغاء تقديمك"
                message = await ctx.author.send(embed=discord.Embed(
                    description=m,
                    color=discord.Color.green()
                ))
                await message.add_reaction("✅")
                await message.add_reaction("❎")

                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in ["✅", "❎"]

                try:
                    reaction, user = await self.client.wait_for("reaction_add", timeout=60, check=check)

                    if str(reaction.emoji) == "✅":
                        await channel.send(embed=embed)
                        m = "✅ Your submit has been sent successfully"
                        if lang == "ar":
                            m = "✅ تم ارسال تقديمك في نجاح"
                        await message.edit(embed=discord.Embed(
                            description=m,
                            color=discord.Color.green()
                        ))
                    elif str(reaction.emoji) == "❎":
                        m = "❌ Your submit has been cancel"
                        if lang == "ar":
                            m = "❌ تم الغاء تقديمك"
                        await message.edit(embed=discord.Embed(
                            description=m,
                            color=discord.Color.red()
                        ))
                        pass
                    else:
                        await message.remove_reaction(reaction, user)

                except asyncio.TimeoutError:
                    await message.delete()
            elif str(reaction.emoji) == "🟡":
                embed = discord.Embed(
                    description="**enter your language?**\n:black_circle: : English Language\n:yellow_circle: : لغه عربيه",
                    color=discord.Color.red()
                )
                message = await ctx.author.send(embed=embed)

                await ctx.message.add_reaction('✅')
                lang = "en"

                await message.add_reaction("⚫")
                await message.add_reaction("🟡")

                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in ["⚫", "🟡"]

                try:
                    reaction, user = await self.client.wait_for("reaction_add", timeout=60, check=check)

                    if str(reaction.emoji) == "⚫":
                        lang = "en"
                    elif str(reaction.emoji) == "🟡":
                        lang = "ar"
                    else:
                        await message.remove_reaction(reaction, user)

                except asyncio.TimeoutError:
                    await message.delete()
                channel = self.client.get_channel(config['submit_channel'])  # id channel
                en_random_questions = [
                    "What is the difference between Node.js and JavaScript?",
                    "List two types of database?",
                    "What do you need to create a complete website?",
                    "Mention two general data types in programming?",
                    "What is the variable?",
                    "What is an integer in programming languages?"
                ]
                ar_random_questions = [
                    "ما الفرق بين Node.js و JavaScript؟",
                    "اذكر نوعين من قواعد البيانات في البرمجه؟",
                    "ما الذي تحتاجه لإنشاء موقع ويب كامل؟",
                    "أذكر نوعين من انواع البيانات في البرمجة؟",
                    "ما هو المتغير في لغات البرمجه؟",
                    "ما هو تعريف العدد في لغات البرمجة؟",
                ]
                en_questions = [
                    '1️⃣ | Write your name now:',
                    '2️⃣ | Write your age now:',
                    '3️⃣ | Write your name language now:',
                    '4️⃣ | Send us a project or no bot that you designed yourself (if you have taken the bot from someone, you will be rejected):',
                    '5️⃣ | {}:'.format(random.choice(en_random_questions)),
                    '6️⃣ | Before completing the application, please read the laws from here <#781902561333870623>',
                ]
                ar_questions = [
                    '1️⃣ | اكتب اسمك الآن: ',
                    '2️⃣ | اكتب عمرك الآن: ',
                    '3️⃣ | اكتب لغتك البرمجيه الآن: ',
                    '4️⃣ | أرسل لنا مشروعًا أو روبوتًا صممته بنفسك (إذا كنت قد أخذت الروبوت من شخص ما ، فسيتم رفضك): ',
                    '5️⃣ | {}: '.format(random.choice(ar_random_questions)),
                    '6️⃣ | قبل استكمال الطلب برجاء قراءة القوانين من هنا <#781902561333870623> ',
                ]
                answers = []
                embed = discord.Embed(
                    description=ctx.author.id,
                    color=ctx.author.color,
                    timestamp=ctx.message.created_at
                )
                m = "You have 3 minutes to answer each question"
                if lang == "ar":
                    m = "لديك 3 دقائق للإجابة على كل سؤال"
                await ctx.author.send(
                    embed=discord.Embed(
                        description=m,
                        color=0xf7072b))

                def check(m):
                    return m.author == ctx.author and m.author == ctx.author and str(m.channel.type) == "private"

                nam = 0
                if lang == "ar":
                    en_questions = ar_questions
                for i in en_questions:
                    nam += 1
                    await ctx.author.send(embed=discord.Embed(
                        description=i,
                        color=0xf7072b).set_author(name=f"{nam}/{len(en_questions)}"))
                    try:
                        msg = await self.client.wait_for('message', timeout=180.0, check=check)
                    except asyncio.TimeoutError:
                        m = 'You have exceeded the time specified for submit'
                        if lang == "ar":
                            m = "لقد تجاوزت الوقت المحدد للإرسال"
                        await ctx.author.send(embed=discord.Embed(
                            description=m,
                            color=0xf7072b))
                        return
                    else:
                        answers.append(msg.content)

                for kay, value in enumerate(en_questions):
                    embed.add_field(
                        name=f"{kay} - {value}:",
                        value=answers[kay],
                        inline=False
                    )
                embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.set_thumbnail(url=ctx.guild.icon_url)
                m = "rect ✅ to send your submit\nrect ❎ to cancel yot submit"
                if lang == "ar":
                    m = "اضغط ✅ لارسال تقديمك\nاضغط ❌ للغاء تقديمك"
                message = await ctx.author.send(embed=discord.Embed(
                    description=m,
                    color=discord.Color.green()
                ))
                await message.add_reaction("✅")
                await message.add_reaction("❎")

                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in ["✅", "❎"]

                try:
                    reaction, user = await self.client.wait_for("reaction_add", timeout=60, check=check)

                    if str(reaction.emoji) == "✅":
                        await channel.send(embed=embed)
                        m = "✅ Your submit has been sent successfully"
                        if lang == "ar":
                            m = "✅ تم ارسال تقديمك في نجاح"
                        await message.edit(embed=discord.Embed(
                            description=m,
                            color=discord.Color.green()
                        ))
                    elif str(reaction.emoji) == "❎":
                        m = "❌ Your submit has been cancel"
                        if lang == "ar":
                            m = "❌ تم الغاء تقديمك"
                        await message.edit(embed=discord.Embed(
                            description=m,
                            color=discord.Color.red()
                        ))
                        pass
                    else:
                        await message.remove_reaction(reaction, user)

                except asyncio.TimeoutError:
                    await message.delete()
            else:
                await message.remove_reaction(reaction, user)

        except asyncio.TimeoutError:
            await message.delete()


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
    client.add_cog(Submit(client))
