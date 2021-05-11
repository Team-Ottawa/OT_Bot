import discord
from discord.ext import commands
import json
import db

with open('./config.json', 'r') as f:
    config = json.load(f)


class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        x = db.DatabaseUsers(self.client, member.id)
        x.insert()
        channel = self.client.get_channel(813850808650432552)  # get channel
        guild = self.client.get_guild(654423706294026270)
        await channel.send("""
> Welcome %s to OTTAWA server, please go to <#781902561333870623> to learn how you can verified yourself!
> You are the number member `%s`""" % (member.mention, guild.member_count))

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.channel.id != 813850372468506694:
            return
        if ctx.author.bot:
            return
        await ctx.add_reaction("<a:love:748518976371425300>")


def setup(client):
    client.add_cog(Welcome(client))
