import discord
from discord.ext import commands
import config
from discord.http import Route
from discord_ui.cogs import slash_cog


class YouTube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def create_invite(self, channel_id, target_application_id):
        route = Route("POST", f"/channels/{channel_id}/invites")
        re = await self.bot.http.request(
            route,
            json={
                "max_age": 3600,
                "max_uses": 0,
                "target_application_id": str(target_application_id),
                "target_type": 2,
                "temporary": False,
                "validate": None
            })
        return f"https://discord.gg/{re['code']}"

    @slash_cog(
        name="youtube",
        description="create youtube watch from voice channel",
        guild_ids=[config.guild_id]
    )
    async def youtube(self, ctx):
        voice_channel = ctx.author.voice
        if not voice_channel:
            return await ctx.respond("please join voice channel", hidden=True)
        url = await self.create_invite(voice_channel.channel.id, "755600276941176913")
        embed = discord.Embed(
            description=f"Playing youtube [click here]({url})"
        )
        await ctx.respond(embed=embed)

    @slash_cog(
        name="betrayal",
        description="create betrayal playing from voice channel",
        guild_ids=[config.guild_id]
    )
    async def betrayal(self, ctx):
        voice_channel = ctx.author.voice
        if not voice_channel:
            return await ctx.respond("please join voice channel", hidden=True)
        url = await self.create_invite(voice_channel.channel.id, "773336526917861400")
        embed = discord.Embed(
            description=f"[click here]({url})"
        )
        await ctx.respond(embed=embed)

    @slash_cog(
        name="fishington",
        description="create betrayal fishington from voice channel",
        guild_ids=[config.guild_id]
    )
    async def fishington(self, ctx):
        voice_channel = ctx.author.voice
        if not voice_channel:
            return await ctx.respond("please join voice channel", hidden=True)
        url = await self.create_invite(voice_channel.channel.id, "814288819477020702")
        embed = discord.Embed(
            description=f"[click here]({url})"
        )
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(YouTube(bot))
