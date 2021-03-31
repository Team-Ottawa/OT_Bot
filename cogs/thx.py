import discord
from discord.ext import commands, tasks
import db
import asyncio

list_ = []


class Thx(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='thx', aliases=['thanks', "شكر"])
    @commands.guild_only()
    async def thx_command(self, ctx, user: discord.Member):
        if user == ctx.author:
            await ctx.send("ممنوع تشكر نفسك يا طفل")
            return
        if ctx.author.id in list_:
            await ctx.send("you can thx the user after two hours 🙃.")
            return
        if user.bot:
            await ctx.send("this user is bot 🙃.")
            return
        thanks = db.get_thx(user)
        db.cr.execute("UPDATE users SET thanks = ? WHERE user_id = ?", (thanks+1, user.id))
        db.db.commit()
        await ctx.send(f"done thanks {user.mention}, thx count is `{db.get_thx(user)}`")
        list_.append(ctx.author.id)
        await asyncio.sleep(7200)
        list_.remove(ctx.author.id)


def setup(client):
    client.add_cog(Thx(client))
