import discord
from discord.ext import commands
import config
import db


class Welcome(commands.Cog):
    def __init__(self, client, tracker):
        self.client = client
        self.tracker = tracker

    @commands.Cog.listener()
    async def on_member_join(self, member):
        inviter = await self.tracker.fetch_inviter(member)
        x = db.DatabaseUsers(self.client, member.id)
        x.insert()
        channel = self.client.get_channel(843882881104740363)  # get channel
        guild = self.client.get_guild(843865725886398554)
        await channel.send("""
> Welcome %s to OTTAWA server, please go to <#860841465404194826> !
> Invited by : %s
> You are the number member `%s`""" % (member.mention, inviter, guild.member_count))


def setup(client):
    client.add_cog(Welcome(client, client.tracker))
