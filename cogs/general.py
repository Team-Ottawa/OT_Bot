import discord
from discord.ext import commands
import time


replay = {
    "اوتاوا": "يا هلا",
    "صقر": "يا عمر صفر",
    "حازم": "اسطوره البايثون عطه لكزز",
    "بترولي": "يعني يوسف يعني طيران يعني حبيبي والله",
    "يوسف": "يعني بترولي يعني طيران يعني حبيبي والله",
    "-": "**Welcome To Server Ottawa Please Check <#781902561333870623> <:b9c0dcde98313119:762315185670062121> !**",
    ".": "**Welcome To Server Ottawa Please Check <#781902561333870623> <:b9c0dcde98313119:762315185670062121> !**"
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

    @commands.command(name='len', help='length your arg')
    @commands.guild_only()
    async def length(self, ctx, *, arg):
        await ctx.send('Your message is `{}` characters long.'.format(str(len(arg))))

    @length.error
    async def length_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("error")
    #
    # @commands.command(aliases=["id", "userinfo"], help='show user info')
    # async def user(self, ctx, member: discord.Member = None):
    #
    #     member = ctx.author if not member else member
    #
    #     embed = discord.Embed(
    #         timestamp=ctx.message.created_at,
    #         color=ctx.author.color
    #     )
    #
    #     embed.set_author(
    #         name=self.client.user,
    #         url="https://discord.com/oauth2/authorize?client_id=738120633430573176&permissions=8&scope=bot",
    #         icon_url=self.client.user.avatar_url)
    #     embed.set_thumbnail(url=member.avatar_url)
    #     embed.set_footer(
    #         text=f"Requested by {ctx.author}",
    #         icon_url=ctx.author.avatar_url)
    #     embed.add_field(name="{} ╎ Member:".format(self.client.get_emoji(795052145635622942)), value=member.mention)
    #     embed.add_field(name="🆔 ╎ ID:", value=member.id)
    #     embed.add_field(name="{} ╎ Join At:".format(self.client.get_emoji(795053266111168562)),
    #                     value=member.created_at.strftime("%Y/%m/%d"))
    #     embed.add_field(name="{} ╎ Join Server At:".format(self.client.get_emoji(795053825395654666)),
    #                     value=member.joined_at.strftime("%Y/%m/%d"))
    #     badges = ""
    #     for i in list(iter(member.public_flags)):
    #         if i[1] and i[0] == "staff":
    #             badges += (str(self.client.get_emoji(795021566375231508)))
    #         if i[1] and i[0] == "partner":
    #             badges += (str(self.client.get_emoji(795021566668701706)))
    #         if i[1] and i[0] == "early_supporter":
    #             badges += (str(self.client.get_emoji(795021566387814420)))
    #         if i[1] and i[0] == "bug_hunter":
    #             badges += (str(self.client.get_emoji(762364793361006603)))
    #         if i[1] and i[0] == "bug_hunter_level_2":
    #             badges += (str(self.client.get_emoji(795021566253596702)))
    #         if i[1] and i[0] == "early_verified_bot_developer":
    #             badges += (str(self.client.get_emoji(795021566177968148)))
    #         if i[1] and i[0] == "verified_bot":
    #             badges += (str(self.client.get_emoji(795021566072717332)))
    #         if i[1] and i[0] == "hypesquad":
    #             badges += (str(self.client.get_emoji(795021566076780564)))
    #         if i[1] and i[0] == "hypesquad_bravery":
    #             badges += (str(self.client.get_emoji(795021565975986181)))
    #         if i[1] and i[0] == "hypesquad_brilliance":
    #             badges += (str(self.client.get_emoji(795021565800480789)))
    #         if i[1] and i[0] == "hypesquad_balance":
    #             badges += (str(self.client.get_emoji(795021565901144084)))
    #         if i[1] and i[0] == "nitro":
    #             badges += (str(self.client.get_emoji(795021565901144084)))
    #         if i[1] and i[0] == "bot":
    #             badges += (str(self.client.get_emoji(795047209111388190)))
    #         else:
    #             badges += ""
    #     if badges == "":
    #         badges = "None"
    #     embed.add_field(name="{} ╎ Badges:".format(self.client.get_emoji(795054399944130620)), value=badges)
    #     status = ""
    #     if member.status == discord.Status.online:
    #         status += str(self.client.get_emoji(795225784637587488))
    #     elif member.status == discord.Status.offline:
    #         status += str(self.client.get_emoji(795225784850579456))
    #     elif member.status == discord.Status.idle:
    #         status += str(self.client.get_emoji(795225784649383947))
    #     elif member.status == discord.Status.dnd:
    #         status += str(self.client.get_emoji(795225784758697985))
    #     else:
    #         status += str(self.client.get_emoji(795225784947048478))
    #
    #     embed.add_field(name="⁉ ╎ Status:", value=status)
    #     roles = " ".join([role.mention for role in member.roles if role != ctx.guild.default_role])
    #     roles = "Nothing" if not roles else roles
    #     embed.add_field(
    #         name="{} ╎ Roles ({}):".format(self.client.get_emoji(795054968700403712), len(member.roles) - 1),
    #         value=roles, inline=False)

    @commands.command()
    @commands.guild_only()
    async def github(self, ctx):
        await ctx.send("https://github.com/Team-Ottawa")

    @commands.command()
    @commands.guild_only()
    async def support(self, ctx, member: discord.Member):
        embed = discord.Embed(
            description="**how to get help:\n<#804730910687756378>\n\n**كيف يمككني طلب المساعده؟**\n<#804730910687756378>"
        )
        await ctx.send(member.mention, embed=embed)

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.content in replay:
            await ctx.channel.send(replay[ctx.content])
        # elif ctx.content == ".":
        #     m = f"Welcome To Server | > [OTTAWA || اوتاوا]\n\n        Join This Room To Read Rules Server | >  <#781902561333870623>\n        Join This Room To Read News Server | > <#799601584681517126>\n\n        Have Fun | > {self.client.get_emoji(789022158739341322)}"
        #     await ctx.channel.send(f"{m} {self.client.get_emoji(779839267617636373)}\n{ctx.author.mention}")
        else:
            pass


def setup(client):
    client.add_cog(General(client))
