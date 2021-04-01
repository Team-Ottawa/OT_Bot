import discord
from discord.ext import commands, tasks
import db
import re


def convert(timer):
    pos = ["s", "m", "h", "d", "mo", "y"]
    time_dict = {"s": 1, "m": 60, "h": 60 * 60, "d": 3600 * 24, "mo": 216000 * 30, "y": 31536000}
    # unit = timer[-1]
    unit = re.search(r"s|mo|h|d|m|y", timer)
    if unit.group() not in pos:
        return None
    try:
        val = int(timer.translate({ord(unit.group()): None}))
    except:
        return None
    return val * time_dict[unit.group()]


def convert_to_timer(timer):
    time_dict = {"s": 1, "m": 60, "h": 3600, "d": 86400, "mo": 2592000, "y": 31536000}
    for i in time_dict:
        if timer <= time_dict[i]:
            print(time_dict[i])
            print(int(4750504 / timer))
            return f"{int(time_dict[i] / timer)}{i}"
        continue


class Vip(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help='to show your vip time ended')
    @commands.guild_only()
    async def myvip(self, ctx):
        data = db.cr.execute("SELECT * FROM vip").fetchall()
        d = [i[0] for i in data]
        if ctx.author.id not in d:
            await ctx.send("حمبي انت ما عندك vip")
            return
        time = db.get_vip(ctx.author)
        # t = ""
        # if time >= 31536000:
        #     t = f"{int(time / 60 / 60 / 24 / 365)}y"
        # elif time >= 2592000:
        #     t = f'{int(time / 60 / 60 / 24 / 30)}mo'
        # elif time >= 86400:
        #     t = f"{int(time / 60 / 60 / 24)}d"
        # elif time >= 3600:
        #     t = f"{int(time / 60 / 60)}h"
        # elif time >= 60:
        #     t = f"{int(time / 60)}m"
        # elif time < 60:
        #     t = f"{time}s"
        await ctx.send('حمبي ضل لك {}'.format(convert_to_timer(time)))

    @commands.command(name='setvip', aliases=["addvip"], hidden=True)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def set_vip(self, ctx, user: discord.Member, time):
        db.cr.execute("INSERT OR IGNORE INTO vip(user_id, user_name) VALUES(?, ?)", (
            user.id,
            user.name))
        db.db.commit()
        db.cr.execute("UPDATE vip SET vip_time = ? WHERE user_id = ?", (db.get_vip(user)+convert(time), user.id))
        db.db.commit()
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
    @commands.has_permissions(administrator=True)
    async def remove_vip(self, ctx, user: discord.Member):
        db.cr.execute("UPDATE vip SET vip_time = ? WHERE user_id = ?", (1, user.id))
        db.db.commit()
        await user.remove_roles(self.client.get_guild(654423706294026270).get_role(811547143806255134))
        await ctx.send(f"done remove vip to {user.mention}")

    @tasks.loop(seconds=1)
    async def vip(self):
        data = db.cr.execute("SELECT * FROM vip").fetchall()
        for i in data:
            if i[2] <= 0:
                user = self.client.get_guild(654423706294026270).get_member(i[0])
                vip_log = self.client.get_channel(826863222510190614)
                db.cr.execute("DELETE FROM vip WHERE user_id = ?", (i[0],))
                db.db.commit()
                await user.remove_roles(self.client.get_guild(654423706294026270).get_role(811547143806255134))
                await vip_log.send(embed=discord.Embed(
                    title="end vip",
                    description=f"**User:** {user.mention}",
                    color=discord.Color.red(),
                ))
                try:
                    await user.send("**Your __@VIP code__ has been ended, to buy again content owners role @Founder.**")
                except:
                    continue
                continue
            new_data = i[2] - 1
            db.cr.execute("UPDATE vip SET vip_time = ? WHERE user_id = ?", (new_data, i[0]))
            db.db.commit()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.vip.start()


def setup(client):
    client.add_cog(Vip(client))

