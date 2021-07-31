import discord
from discord.ext import commands
from captcha.image import ImageCaptcha
import random
import db
import asyncio
from discord_components import Button, DiscordComponents, InteractionType, ButtonStyle
import datetime


class CaptchaGenerator:
    def __init__(self):
        self.image = ImageCaptcha(width=280, height=90)
        self._id = ''.join(random.choice("1234567890") for _ in range(6))

    @property
    def generator(self):
        self.image.write(self._id, "captcha.png")
        return "captcha.png"

    @property
    def code(self):
        return self._id


class Coins(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def setup(self, ctx):
        embed = discord.Embed(
            title="Free coins :moneybag:",
            description="> **Gifts :gift:**\nClick to button get to get free coins"
        )
        await ctx.send(
            embed=embed,
            components=[
                Button(style=ButtonStyle.green, label="free coins", id="5"),
            ]
        )

    @commands.Cog.listener()
    async def on_button_click(self, res):
        # if isinstance(res.component.id, str):
        #     return
        if res.component.id == "5":
            x = db.Coins(self.client, res.author.id)
            if x.check:
                random_number = random.randint(50, 150)
                coins = x.info.get("coins") + random_number
                x.update_where("coins", coins)
                x.update_where("timestamp", datetime.datetime.now().timestamp() + 1800)
                await res.respond(
                    type=InteractionType.ChannelMessageWithSource,
                    content="Your got `%s` its free" % coins
                )
                return
            old_timestamp = x.info.get("timestamp")
            now = datetime.datetime.now().timestamp()
            value = old_timestamp - now
            await res.respond(
                type=InteractionType.ChannelMessageWithSource,
                content="pls request again %s" % datetime.datetime.fromtimestamp(value).strftime("%H:%M:%S")
            )
            return

    @commands.command(name='add_coins')
    @commands.guild_only()
    @commands.is_owner()
    async def add_coins(self, ctx, member: discord.Member, count: int):
        x = db.Coins(self.client, member.id)
        new_coins = x.info.get("coins") + count
        x.update_where("coins", new_coins)
        await ctx.send("`%s` coins has been added successfully %s to %s" % (
            count,
            self.client.get_emoji(844084556360319008),
            member.mention
        ))

    @commands.command(name='coins')
    @commands.guild_only()
    async def coins(self, ctx, member: discord.Member = None, count: int = None):
        if not member and not count:
            x = db.Coins(self.client, ctx.author.id)
            coins = x.info.get("coins")
            coins = coins if coins else 0
            await ctx.send("Your coins == `%s`:coin:" % coins)
            return
        if not count:
            x = db.Coins(self.client, member.id)
            coins = x.info.get("coins")
            coins = coins if coins else 0
            await ctx.send("coins from **%s** == `%s`:coin:" % (member, coins))
            return
        member_coins = db.Coins(self.client, ctx.author.id).info.get("coins")
        if member_coins < count:
            raise commands.errors.CheckFailure("You don't have the required amount")
        if count <= 0:
            return await ctx.send("The value is not enough")
        captcha = CaptchaGenerator()
        file = captcha.generator
        code = captcha.code
        _msg = await ctx.send("Type the captcha number", file=discord.File(file))

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author
        try:
            msg = await self.client.wait_for('message', timeout=15.0, check=check)
        except asyncio.TimeoutError:
            await _msg.delete()
            return
        else:
            await _msg.delete()
            await msg.delete()
            if msg.content != str(code):
                return await ctx.send(":no: Sending failed due to wrong verification code")
            x = db.Coins(self.client, ctx.author.id)
            await x.transfer(member.id, count)
            await ctx.send("%s | transfer `%s` to %s" % (
                self.client.get_emoji(844084556360319008),
                count,
                member.mention
            ))


def setup(client):
    DiscordComponents(client)
    client.add_cog(Coins(client))


