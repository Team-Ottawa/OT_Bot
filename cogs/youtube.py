import discord
from discord.ext import commands
import requests
import config


class YouTube(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='youtube')
    @commands.guild_only()
    async def youtube(self, ctx):
        chn = ctx.author.voice
        if chn == None:
            return await ctx.send("please join voice channel")
        channel = chn.channel
        x = requests.post(
            "https://discord.com/api/v8/channels/%s/invites" % channel.id,
            json={
                "max_age": 3600,
                "max_uses": 0,
                "target_application_id": "755600276941176913",
                "target_type": 2,
                "temporary": False,
                "validate": None
            },
            headers={
                "Authorization": "Bot %s" % config.token,
                "Content-Type": "application/json"
            }
        )
        code = x.json()["code"]
        embed = discord.Embed(
            description="Playing youtube [click here](https://discord.gg/%s)" % code
        )
        await ctx.send(embed=embed)

    @commands.command(name='betrayal')
    @commands.guild_only()
    async def betrayal(self, ctx):
        chn = ctx.author.voice
        if chn == None:
            return await ctx.send("please join voice channel")
        channel = chn.channel
        x = requests.post(
            "https://discord.com/api/v8/channels/%s/invites" % channel.id,
            json={
                "max_age": 3600,
                "max_uses": 0,
                "target_application_id": "773336526917861400",
                "target_type": 2,
                "temporary": False,
                "validate": None
            },
            headers={
                "Authorization": "Bot %s" % config.token,
                "Content-Type": "application/json"
            }
        )
        code = x.json()["code"]
        embed = discord.Embed(
            description="[click here](https://discord.gg/%s)" % code
        )
        await ctx.send(embed=embed)

    @commands.command(name='fishington')
    @commands.guild_only()
    async def fishington(self, ctx):
        chn = ctx.author.voice
        if chn == None:
            return await ctx.send("please join voice channel")
        channel = chn.channel
        x = requests.post(
            "https://discord.com/api/v8/channels/%s/invites" % channel.id,
            json={
                "max_age": 3600,
                "max_uses": 0,
                "target_application_id": "814288819477020702",
                "target_type": 2,
                "temporary": False,
                "validate": None
            },
            headers={
                "Authorization": "Bot %s" % config.token,
                "Content-Type": "application/json"
            }
        )
        code = x.json()["code"]
        embed = discord.Embed(
            description="[click here](https://discord.gg/%s)" % code
        )
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(YouTube(client))
