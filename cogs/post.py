import discord
from discord.ext import commands
import asyncio
import json

with open('./config.json', 'r') as f:
    config = json.load(f)


class post(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 300, commands.BucketType.user)
    @commands.has_any_role(config['coder_role_name'])
    async def js(self, ctx):

        channel = self.client.get_channel(config["js"]['js_channel'])  # id channel 779371022939848775
        channel2 = self.client.get_channel(config["js"]['js_temp'])  # id channel

        questions_1 = [
            'Write the code now without putting tags:',
            'Write the copyright:',
            'Write the code title',
            'Write the code description',
            'Confirm Code Share (Yes / No)']
        answers = []
        await ctx.author.send(embed=discord.Embed(
            description="You have 3 minutes to answer each question",
            color=0xf7072b
        ))
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
                    description='You have exceeded the specified time',
                    color=0xf7072b))
                return
            else:
                answers.append(msg.content)
        if answers[4] == 'yes' or answers[4] == "Yes" or answers[4] == "YES":
            await ctx.author.send(embed=discord.Embed(
                    description='Your code has been shared with everyone',
                    color=0xf7072b))
            embed = discord.Embed(description='''
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
```js\n{}\n```
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
<:aea4f8d034911298:761876595770130452> **codes** : {}
<:cb485bd4e5010caa:761876609358757918> **Description** : {}
<:a66b5fda582d1606:761876608196804609> **shared By** : {}
<:73aff2681a13b61a:761876614761807883> **copyrights** : {}
<:330e0c76068aa97d:761876595006767104> **language** : javascript
    '''.format(answers[0], answers[2], answers[3], ctx.author.mention, answers[1]))

            my_msg = await channel.send("<@&{}>".format(config["mention_code_role"]), embed=embed)
            await channel2.send(embed=embed)
            await channel2.send(
                'https://cdn.discordapp.com/attachments/754398470558842930/771086560941965322/42_E25EB2C-1.gif')
            await my_msg.add_reaction('<a:up__:775832508280733716>')
            await my_msg.add_reaction('<a:down__:775832765518184488>')
            await channel.send(
                'https://cdn.discordapp.com/attachments/754398470558842930/771086560941965322/42_E25EB2C-1.gif')
            return
        elif answers[4] == 'no' or answers[4] == 'No' or answers[4] == 'NO':
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

    @commands.has_any_role(config['coder_role_name'])
    @js.error
    async def js_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            pass
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.author.send(embed=discord.Embed(
                description="❌ Please open your DM before applying and reapply again after 5 minutes",
                color=0xf7072b
            ))
        if isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            await ctx.send(embed=discord.Embed(
                description="❌ It seems that you have chosen the wrong answer. You can reapply again after {}".format("%02d minutes, %02d seconds" % (m, s)),
                color=0xf7072b
            ))
        else:
            print(error)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 300, commands.BucketType.user)
    @commands.has_any_role(config['coder_role_name'])
    async def py(self, ctx):

        channel = self.client.get_channel(config["py"]['py_channel'])  # id channel
        channel2 = self.client.get_channel(config["py"]['py_temp'])  # id channel
        questions_1 = [
            'Write the code now without putting tags:',
            'Write the copyright:',
            'Write the code title',
            'Write the code description',
            'Confirm Code Share (Yes / No)']
        answers = []
        await ctx.author.send(embed=discord.Embed(
            description="You have 3 minutes to answer each question",
            color=0xf7072b
        ))
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
                    description='You have exceeded the specified time',
                    color=0xf7072b))
                return
            else:
                answers.append(msg.content)
        if answers[4] == 'yes' or answers[4] == "Yes" or answers[4] == "YES":
            await ctx.author.send(embed=discord.Embed(
                description='Your code has been shared with everyone',
                color=0xf7072b))
            embed = discord.Embed(description='''
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
```py\n{}\n```
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
<:aea4f8d034911298:761876595770130452> **codes** : {}
<:cb485bd4e5010caa:761876609358757918> **Description** : {}
<:a66b5fda582d1606:761876608196804609> **shared By** : {}
<:73aff2681a13b61a:761876614761807883> **copyrights** : {}
<:330e0c76068aa97d:761876595006767104> **language** : python
    '''.format(answers[0], answers[2], answers[3], ctx.author.mention, answers[1]))

            my_msg = await channel.send("<@&{}>".format(config["mention_code_role"]), embed=embed)
            await channel2.send(embed=embed)
            await channel2.send(
                'https://cdn.discordapp.com/attachments/754398470558842930/771086560941965322/42_E25EB2C-1.gif')
            await my_msg.add_reaction('<a:up__:775832508280733716>')
            await my_msg.add_reaction('<a:down__:775832765518184488>')
            await channel.send(
                'https://cdn.discordapp.com/attachments/754398470558842930/771086560941965322/42_E25EB2C-1.gif')
            return
        elif answers[4] == 'no' or answers[4] == 'No' or answers[4] == 'NO':
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

    @commands.has_any_role(config['coder_role_name'])
    @py.error
    async def py_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            pass
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.author.send(embed=discord.Embed(
                description="❌ Please open your DM before applying and reapply again after 5 minutes",
                color=0xf7072b
            ))
        if isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            await ctx.send(embed=discord.Embed(
                description="❌ It seems that you have chosen the wrong answer. You can reapply again after {}".format("%02d minutes, %02d seconds" % (m, s)),
                color=0xf7072b
            ))
        else:
            print(error)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 300, commands.BucketType.user)
    @commands.has_any_role(config['coder_role_name'])
    async def dbd(self, ctx):
        channel = self.client.get_channel(config["dbd"]['dbd_channel'])  # id channel
        channel2 = self.client.get_channel(config["dbd"]['dbd_temp'])  # id channel

        questions_1 = [
            'Write the code now without putting tags:',
            'Write the copyright:',
            'Write the code title',
            'Write the code description',
            'Confirm Code Share (Yes / No)']
        answers = []
        await ctx.author.send(embed=discord.Embed(
            description="You have 3 minutes to answer each question",
            color=0xf7072b
        ))
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
                    description='You have exceeded the specified time',
                    color=0xf7072b))
                return
            else:
                answers.append(msg.content)
        if answers[4] == 'yes' or answers[4] == "Yes" or answers[4] == "YES":
            await ctx.author.send(embed=discord.Embed(
                description='Your code has been shared with everyone',
                color=0xf7072b))
            embed = discord.Embed(description='''
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
```d\n{}\n```
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
<:aea4f8d034911298:761876595770130452> **codes** : {}
<:cb485bd4e5010caa:761876609358757918> **Description** : {}
<:a66b5fda582d1606:761876608196804609> **shared By** : {}
<:73aff2681a13b61a:761876614761807883> **copyrights**: {}
<:330e0c76068aa97d:761876595006767104> **language** : dbd
'''.format(answers[0], answers[2], answers[3], ctx.author.mention, answers[1]))

            my_msg = await channel.send("<@&{}>".format(config["mention_code_role"]), embed=embed)
            await channel2.send(embed=embed)
            await channel2.send('https://cdn.discordapp.com/attachments/754398470558842930/771086560941965322/42_E25EB2C-1.gif')
            await my_msg.add_reaction('<a:up__:775832508280733716>')
            await my_msg.add_reaction('<a:down__:775832765518184488>')
            await channel.send('https://cdn.discordapp.com/attachments/754398470558842930/771086560941965322/42_E25EB2C-1.gif')
            return
        elif answers[4] == 'no' or answers[4] == 'No' or answers[4] == 'NO':
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

    @commands.has_any_role(config['coder_role_name'])
    @dbd.error
    async def dbd_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            pass
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.author.send(embed=discord.Embed(
                description="❌ Please open your DM before applying and reapply again after 5 minutes",
                color=0xf7072b
            ))
        if isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            await ctx.send(embed=discord.Embed(
                description="❌ It seems that you have chosen the wrong answer. You can reapply again after {}".format("%02d minutes, %02d seconds" % (m, s)),
                color=0xf7072b
            ))
        else:
            print(error)

    @commands.command()
    @commands.guild_only()
    @commands.has_any_role(config['coder_role_name'])
    async def web(self, ctx):
        channel = self.client.get_channel(config["web"]['web_channel'])  # id channel
        channel2 = self.client.get_channel(config["web"]['web_temp'])
        questions_1 = [
            'Write the code now without putting tags:',
            'Write the copyright:',
            'Write the code title',
            'Write the code description',
            'Confirm Code Share (Yes / No)']
        answers = []
        await ctx.author.send(embed=discord.Embed(
            description="You have 3 minutes to answer each question",
            color=0xf7072b
        ))
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
                    description='You have exceeded the specified time',
                    color=0xf7072b))
                return
            else:
                answers.append(msg.content)
        if answers[4] == 'yes' or answers[4] == "Yes" or answers[4] == "YES":
            await ctx.author.send(embed=discord.Embed(
                description='Your code has been shared with everyone',
                color=0xf7072b))
            embed = discord.Embed(description='''
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
```html\n{}\n```
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
<:aea4f8d034911298:761876595770130452> **codes** : {}
<:cb485bd4e5010caa:761876609358757918> **Description** : {}
<:a66b5fda582d1606:761876608196804609> **shared By** : {}
<:73aff2681a13b61a:761876614761807883> **copyrights**: {}
<:330e0c76068aa97d:761876595006767104> **language** : html/css 
'''.format(answers[0], answers[2], answers[3], ctx.author.mention, answers[1]))
            my_msg = await channel.send("<@&{}>".format(config["mention_code_role"]), embed=embed)
            await channel2.send(embed=embed)
            await my_msg.add_reaction('<a:up__:775832508280733716>')
            await my_msg.add_reaction('<a:down__:775832765518184488>')
            await channel.send('https://cdn.discordapp.com/attachments/754398470558842930/771086560941965322/42_E25EB2C-1.gif')
            return
        elif answers[4] == 'no' or answers[4] == 'No' or answers[4] == 'NO':
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

    @commands.has_any_role(config['coder_role_name'])
    @web.error
    async def web_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            pass
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.author.send(embed=discord.Embed(
                description="❌ Please open your DM before applying and reapply again after 5 minutes",
                color=0xf7072b
            ))
        if isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            await ctx.send(embed=discord.Embed(
                description="❌ It seems that you have chosen the wrong answer. You can reapply again after {}".format("%02d minutes, %02d seconds" % (m, s)),
                color=0xf7072b
            ))
        else:
            print(error)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def post(self, ctx):
        channel = self.client.get_channel(config["post"]['post_channel'])  # id channel
        channel2 = self.client.get_channel(config["post"]['post_temp'])
        await ctx.message.add_reaction('✅')
        questions_1 = [
            'Write the code now without putting tags:',
            'Write the copyright:',
            'Write the code title',
            'Write the code description',
            'Confirm Code Share (Yes / No)']
        answers = []
        enter_nam = [
            "1",
            "2",
            "3",
            "4"
        ]
        loop_nam = [1]

        def check(m):
            return m.author == ctx.author and m.author == ctx.author

        for i in loop_nam:
            await ctx.author.send(embed=discord.Embed(
                title="Choose the appropriate number for the language in which you want to publish the code",
                description="1 => js\n2 => py\n3 => web(html, css)\n4 => dbd",
                color=0xf7072b))
            try:
                msg = await self.client.wait_for('message', timeout=180.0, check=check)
            except asyncio.TimeoutError:
                await ctx.author.send(embed=discord.Embed(
                        description='You have exceeded the specified time',
                        color=0xf7072b))
                return
            else:
                if msg.content in enter_nam:
                    n = int(msg.content)
                elif msg.content not in enter_nam:
                    await ctx.author.send(embed=discord.Embed(
                        description="It seems that you made a mistake in choosing the language, you can try after five minutes",
                        color=0xf7072b))
                    break
        if n == 1:

            await ctx.author.send(embed=discord.Embed(
                description="You have 3 minutes to answer each question",
                color=0xf7072b
            ))

            for i in questions_1:
                await ctx.author.send(embed=discord.Embed(
                    description=i,
                    color=0xf7072b))
                try:
                    msg = await self.client.wait_for('message', timeout=180.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.author.send(embed=discord.Embed(
                        description="It seems that you made a mistake in choosing the language, you can try after five minutes",
                        color=0xf7072b))
                    return
                else:
                    answers.append(msg.content)
            if answers[4] == 'yes' or answers[4] == "Yes" or answers[4] == "YES":
                await ctx.author.send(embed=discord.Embed(
                    description='Your code has been shared with everyone',
                    color=0xf7072b))
                embed = discord.Embed(description='''
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
```js\n{}\n```
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
<:aea4f8d034911298:761876595770130452> **codes** : {}
<:cb485bd4e5010caa:761876609358757918> **Description** : {}
<:a66b5fda582d1606:761876608196804609> **Shard By** : {}
<:73aff2681a13b61a:761876614761807883> **copyrights**: {}
<:330e0c76068aa97d:761876595006767104> **language** : javascript
'''.format(answers[0], answers[2], answers[3], ctx.author.mention, answers[1]), color=0xe1ff00)

                my_msg = await channel.send(embed=embed)
                await channel2.send(embed=embed)
                await channel2.send(
                    'https://cdn.discordapp.com/attachments/754398470558842930/771086560941965322/42_E25EB2C-1.gif')
                await my_msg.add_reaction('<a:up__:775832508280733716>')
                await my_msg.add_reaction('<a:down__:775832765518184488>')
                await channel.send(
                    'https://cdn.discordapp.com/attachments/754398470558842930/771086560941965322/42_E25EB2C-1.gif')
                return
            elif answers[4] == 'no' or answers[4] == 'No' or answers[4] == 'NO':
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

        if n == 2:

            await ctx.author.send(embed=discord.Embed(
                description="You have 3 minutes to answer each question",
                color=0xf7072b
            ))

            for i in questions_1:
                await ctx.author.send(embed=discord.Embed(
                    description=i,
                    color=0xf7072b))
                try:
                    msg = await self.client.wait_for('message', timeout=180.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.author.send(embed=discord.Embed(
                        description="It seems that you made a mistake in choosing the language, you can try after five minutes",
                        color=0xf7072b))
                    return
                else:
                    answers.append(msg.content)
            if answers[4] == 'yes' or answers[4] == "Yes" or answers[4] == "YES":
                await ctx.author.send(embed=discord.Embed(
                    description='Your code has been shared with everyone',
                    color=0xf7072b))
                embed = discord.Embed(description='''
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
```py\n{}\n```
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
<:aea4f8d034911298:761876595770130452> **codes** : {}
<:cb485bd4e5010caa:761876609358757918> **Description** : {}
<:a66b5fda582d1606:761876608196804609> **Shard By** : {}
<:73aff2681a13b61a:761876614761807883> **copyrights**: {}
<:330e0c76068aa97d:761876595006767104> **language** : python
'''.format(answers[0], answers[2], answers[3], ctx.author.mention, answers[1]), color=0x5000bf)

                my_msg = await channel.send(embed=embed)
                await channel2.send(embed=embed)
                await channel2.send(
                    'https://cdn.discordapp.com/attachments/754398470558842930/771086560941965322/42_E25EB2C-1.gif')
                await my_msg.add_reaction('<a:up__:775832508280733716>')
                await my_msg.add_reaction('<a:down__:775832765518184488>')
                await channel.send(
                    'https://cdn.discordapp.com/attachments/754398470558842930/771086560941965322/42_E25EB2C-1.gif')
                return
            elif answers[4] == 'no' or answers[4] == 'No' or answers[4] == 'NO':
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

        if n == 3:

            await ctx.author.send(embed=discord.Embed(
                description="You have 3 minutes to answer each question",
                color=0xf7072b
            ))

            for i in questions_1:
                await ctx.author.send(embed=discord.Embed(
                    description=i,
                    color=0xf7072b))
                try:
                    msg = await self.client.wait_for('message', timeout=180.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.author.send(embed=discord.Embed(
                        description="It seems that you made a mistake in choosing the language, you can try after five minutes",
                        color=0xf7072b))
                    return
                else:
                    answers.append(msg.content)
            if answers[4] == 'yes' or answers[4] == "Yes" or answers[4] == "YES":
                await ctx.author.send(embed=discord.Embed(
                    description='Your code has been shared with everyone',
                    color=0xf7072b))
                embed = discord.Embed(description='''
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
```html\n{}\n```
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
<:aea4f8d034911298:761876595770130452> **codes** : {}
<:cb485bd4e5010caa:761876609358757918> **Description** : {}
<:a66b5fda582d1606:761876608196804609> **Shard By** : {}
<:73aff2681a13b61a:761876614761807883> **copyrights**: {}
<:330e0c76068aa97d:761876595006767104> **language** : html/css
'''.format(answers[0], answers[2], answers[3], ctx.author.mention, answers[1]), color=0xf2180c)

                my_msg = await channel.send(embed=embed)
                await channel2.send(embed=embed)
                await channel2.send(
                    'https://cdn.discordapp.com/attachments/754398470558842930/771086560941965322/42_E25EB2C-1.gif')
                await my_msg.add_reaction('<a:up__:775832508280733716>')
                await my_msg.add_reaction('<a:down__:775832765518184488>')
                await channel.send(
                    'https://cdn.discordapp.com/attachments/754398470558842930/771086560941965322/42_E25EB2C-1.gif')
                return
            elif answers[4] == 'no' or answers[4] == 'No' or answers[4] == 'NO':
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

        if n == 4:
            await ctx.author.send(embed=discord.Embed(
                description="You have 3 minutes to answer each question",
                color=0xf7072b
            ))

            for i in questions_1:
                await ctx.author.send(embed=discord.Embed(
                    description=i,
                    color=0xf7072b))
                try:
                    msg = await self.client.wait_for('message', timeout=180.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.author.send(embed=discord.Embed(
                        description="It seems that you made a mistake in choosing the language, you can try after five minutes",
                        color=0xf7072b))
                    return
                else:
                    answers.append(msg.content)
            if answers[4] == 'yes' or answers[4] == "Yes" or answers[4] == "YES":
                await ctx.author.send(embed=discord.Embed(
                    description='Your code has been shared with everyone',
                    color=0xf7072b))
                embed = discord.Embed(description='''
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
```d\n{}\n```
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
<:aea4f8d034911298:761876595770130452> **codes** : {}
<:cb485bd4e5010caa:761876609358757918> **Description** : {}
<:a66b5fda582d1606:761876608196804609> **Shard By** : {}
<:73aff2681a13b61a:761876614761807883> **copyrights**: {}
<:330e0c76068aa97d:761876595006767104> **language** : dbd
'''.format(answers[0], answers[2], answers[3], ctx.author.mention, answers[1]), color=0x580fd6)

                my_msg = await channel.send(embed=embed)
                await channel2.send(embed=embed)
                await channel2.send(
                    'https://cdn.discordapp.com/attachments/754398470558842930/771086560941965322/42_E25EB2C-1.gif')
                await my_msg.add_reaction('<a:up__:775832508280733716>')
                await my_msg.add_reaction('<a:down__:775832765518184488>')
                await channel.send(
                    'https://cdn.discordapp.com/attachments/754398470558842930/771086560941965322/42_E25EB2C-1.gif')
                return
            elif answers[4] == 'no' or answers[4] == 'No' or answers[4] == 'NO':
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

    @post.error
    async def post_error(self, ctx, error):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.author.send(embed=discord.Embed(
                description="❌ Please open your DM before applying and reapply again after 5 minutes",
                color=0xf7072b
            ))
        if isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            await ctx.send(embed=discord.Embed(
                description="❌ It seems that you have chosen the wrong answer. You can reapply again after {}".format("%02d minutes, %02d seconds" % (m, s)),
                color=0xf7072b
            ))
        else:
            print(error)


def setup(client):
    client.add_cog(post(client))
