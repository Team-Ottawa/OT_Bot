import discord
from discord.ext import commands
import time


replay = {
    "صقر": "يا عمر صقر",
    "حازم": "اسطوره البايثون عطه لكزز",
    "بترولي": "يعني يوسف يعني طيران يعني حبيبي والله",
    "يوسف": "يعني بترولي يعني طيران يعني حبيبي والله",
    "-": "**Welcome To Server Ottawa Please Check <#781902561333870623> <:b9c0dcde98313119:762315185670062121> !**",
    ".": "**Welcome To Server Ottawa Please Check <#781902561333870623> <:b9c0dcde98313119:762315185670062121> !**",
    "السلام عليكم": "وعليكم السلام ورحمة الله وبركاته، نورت السيرفر",
    "السلام عليكم ورحمة الله وبركاته": "وعليكم السلام ورحمة الله وبركاته، النورت السيرفر",
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

    @commands.command(invoke_without_command=True, help='To know the connection speed of the bot on the server')
    @commands.guild_only()
    async def ping(self, ctx):
        before = time.monotonic()
        msg = await ctx.send("pong!")
        ping = (time.monotonic() - before) * 1000
        await msg.edit(content="```c\nTime taken: {}ms\nDiscord API: {}ms```".format(int(ping), round(self.client.latency * 1000)))

    @ping.error
    async def ping_error(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.content in replay:
            await ctx.channel.send(replay[ctx.content])
        if ctx.channel != 813520464872734740:
            return
        if ctx.bot:
            return
        if ctx.message.content == "!verified":
            await ctx.author.add_roles(discord.utils.get(ctx.author.guild.roles, name="Verified"))
            await ctx.channel.send(embed=discord.Embed(
                description="✅ You have been accepted successfully",
                color=0x03ff74
            ))

def setup(client):
    client.add_cog(General(client))
