import discord
from discord.ext import commands
import config
import db
import asyncio
from discord_ui.cogs import slash_cog

list_ = []


class Thx(commands.Cog):
    def __init__(self, client):
        self.client = client

    @slash_cog(
        name="thanks",
        description="to thanks the Helper",
        guild_ids=[config.guild_id]
    )
    async def thx_command(self, ctx, user: discord.Member):
        if user == ctx.author:
            await ctx.respond("ممنوع تشكر نفسك يا طفل")
            return
        if ctx.author.id in list_:
            await ctx.respond("you can thx the user after two hours 🙃.")
            return
        if user.bot:
            await ctx.respond("this user is bot 🙃.")
            return
        x = db.DatabaseUsers(self.client, user.id)
        old_thanks = x.info.get("thanks")
        x.update_where("thanks", int(old_thanks)+1)
        await ctx.respond(f"done thanks {user.mention}, thx count is `{int(old_thanks)+1}`")
        list_.append(ctx.author.id)
        await asyncio.sleep(7200)
        list_.remove(ctx.author.id)


def setup(client):
    client.add_cog(Thx(client))
