import discord
from discord.ext import commands
from PIL import Image
from io import BytesIO
from PIL import ImageFont, ImageDraw, ImageOps
import os
import arabic_reshaper
import json

with open('./config.json', 'r') as f:
    config = json.load(f)


class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.client.get_channel(config['welcome_channel'])  # get channel
        guild = self.client.get_guild(654423706294026270)
        await channel.send("""
> Welcome {} to OTTAWA server, please go to <#813541018107772938> to learn how you can verified yourself!
> You are the number member `{}`
""".format(member.mention, guild.member_count))

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.channel.id != 813850372468506694:
            return
        if ctx.author.bot:
            return

        await ctx.add_reaction("<a:love:748518976371425300>")


def setup(client):
    client.add_cog(Welcome(client))
