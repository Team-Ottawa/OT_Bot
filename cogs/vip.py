import discord
from discord.ext import commands, tasks
import db
import re


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
        data = db.get_all_vip()
        d = [i[0] for i in data]
        if ctx.author.id not in d:
            await ctx.send("حمبي انت ما عندك vip")
            return
        await ctx.send(display_time(db.get_vip(ctx.author)))

    @commands.command(name='setvip', aliases=["addvip"], hidden=True)
    @commands.guild_only()
    @commands.is_owner()
    async def set_vip(self, ctx, user: discord.Member, time):
        db.set_vip(user, convert(time))
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
        db.remove_vip(user.id)
        await user.remove_roles(self.client.get_guild(654423706294026270).get_role(811547143806255134))
        await ctx.send(f"done remove vip to {user.mention}")

    @tasks.loop(seconds=1)
    async def vip(self):
        data = db.get_all_vip()
        for i in data:
            user = self.client.get_guild(654423706294026270).get_member(i[0])
            if user is None:
                db.remove_vip(i[0])
                continue
            if i[1] <= 0:
                db.remove_vip(user.id)
                await user.remove_roles(self.client.get_guild(654423706294026270).get_role(811547143806255134))
                await self.client.get_channel(826863222510190614).send(embed=discord.Embed(
                    title="end vip",
                    description=f"**User:** {user.mention}",
                    color=discord.Color.red(),
                ))
                try:
                    await user.send("**Your __@VIP code__ has been ended, to buy again content owners role @Founder.**")
                    continue
                except:
                    continue
            db.edit_vip(user)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.vip.start()


def setup(client):
    client.add_cog(Vip(client))

