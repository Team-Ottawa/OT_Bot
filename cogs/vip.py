import discord
from discord.ext import commands, tasks
import db
import re
from datetime import datetime
import time


def convert(timer):
    pos = ["s", "m", "h", "d", "mo", "y"]
    time_dict = {"s": 1, "m": 60, "h": 60 * 60, "d": 86400 * 24, "mo": 216000 * 30, "y": 31536000}
    # unit = timer[-1]
    unit = re.search(r"s|mo|h|d|m|y", timer)
    if unit.group() not in pos:
        return None
    try:
        val = int(timer.translate({ord(unit.group()): None}))
    except:
        return None
    return val * time_dict[unit.group()]


# def revers_convert(seconds: int):
#     seconds = seconds % (24 * 3600)
#     hour = seconds // 3600
#     seconds %= 3600
#     minutes = seconds // 60
#     seconds %= 60
#
#     return "%d:%02d:%02d" % (hour, minutes, seconds)
#
#
# n = 12345
# print(convert(n))

intervals = (
    ('year', 31536000),
    ('month', 216000),
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
)


def display_time(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])


class Vip(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help='to show your vip time ended')
    @commands.guild_only()
    async def myvip(self, ctx):
        x = db.DatabaseVip(self.client, ctx.author.id)
        info = x.info
        if info is None:
            await ctx.send("حمبي انت ما عندك vip")
            return
        # _time = datetime.fromtimestamp(info.get("end_at"))
        await ctx.send(info.get("end_at"))
        # print(_time.strftime("year: %Y, month: %m, days: %d"))
        # await ctx.send(str(datetime.fromtimestamp(info.get("end_at")).strftime("year: %Y, month: %m, days: %d")))
        # await ctx.send(time.strftime("year: %Y, month: %m, days: %d", time.gmtime(info.get("time"))))

    @commands.command(name='setvip', aliases=["addvip"], hidden=True)
    @commands.guild_only()
    @commands.is_owner()
    async def set_vip(self, ctx, user: discord.Member, time):
        x = db.DatabaseVip(self.client, user.id)
        end_at = int(datetime.timestamp(datetime.now()) + convert(time))
        timestamp = datetime.fromtimestamp(end_at)
        print(timestamp)
        x.insert(ctx, time, convert(time), timestamp)
        await user.add_roles(self.client.get_guild(654423706294026270).get_role(811547143806255134))
        await ctx.send(f"done add vip to {user.mention}, {time}")
        vip_log = self.client.get_channel(826863222510190614)
        embed = discord.Embed(
            title="new vip",
            description=f"**User:** {user} | {user.id}\n**Data:** {time}\n**By:** {ctx.author.mention}",
            color=discord.Color.green(),
            timestamp=ctx.message.created_at
        )
        await vip_log.send(embed=embed)

    @commands.command(name='removevip', aliases=["revip"], hidden=True)
    @commands.guild_only()
    @commands.is_owner()
    async def remove_vip(self, ctx, user: discord.Member):
        x = db.DatabaseVip(self.client, user.id)
        info = x.info
        x.delete_vip()
        await user.remove_roles(self.client.get_guild(654423706294026270).get_role(811547143806255134))
        await self.client.get_channel(826863222510190614).send(embed=discord.Embed(
            title="remove vip",
            description=f"**User:** %s\n**Add By:** %s\n**Time:** %s\n**Remove By:** %s" % (
                user.mention,
                await self.client.fetch_user(info.get("add_by")),
                info.get("time_str"),
                ctx.author
            ),
            color=discord.Color.red(),
        ))
        await ctx.send(f"done remove vip to {user.mention}")

    @tasks.loop(seconds=2)
    async def vip(self):
        x = db.DatabaseVip(self.client)
        data = x.all
        for i in data:
            _x = db.DatabaseVip(self.client, i.get("_id"))
            _x.update_time()
            user = self.client.get_guild(654423706294026270).get_member(i.get("_id"))
            if user is None:
                _x.delete_vip()
                continue
            if i.get("time") <= 0:
                _x.delete_vip()
                await user.remove_roles(self.client.get_guild(654423706294026270).get_role(811547143806255134))
                await self.client.get_channel(826863222510190614).send(embed=discord.Embed(
                    title="end vip",
                    description=f"**User:** %s\n**Add By:** %s\n**Time:** %s" % (
                        user.mention,
                        await self.client.fetch_user(i.get("add_by")),
                        i.get("time_str")
                    ),
                    color=discord.Color.red(),
                ))
                try:
                    await user.send("**Your __@VIP code__ has been ended, to buy again content owners role @Founder.**")
                    continue
                except:
                    continue

    @commands.Cog.listener()
    async def on_ready(self):
        await self.vip.start()


def setup(client):
    client.add_cog(Vip(client))

