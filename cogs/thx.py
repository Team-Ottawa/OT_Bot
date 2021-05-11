import discord
from discord.ext import commands, tasks
import db
import asyncio

list_ = []


class Thx(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='thx', aliases=['thanks', "شكر"], help='to thanks the Helper')
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
        x = db.DatabaseUsers(self.client, user.id)
        old_thanks = x.info.get("xp")
        x.update_where("thanks", old_thanks+1)
        await ctx.send(f"done thanks {user.mention}, thx count is `{old_thanks+1}`")
        channel = self.client.get_channel(826883667925663794)
        await channel.send(embed=discord.Embed(
            description=f"**By:** {ctx.author.mention}\n**To:** {user.mention}\n**thanks count**: {old_thanks+1}",
            color=discord.Color.green()
        ))
        list_.append(ctx.author.id)
        await asyncio.sleep(7200)
        list_.remove(ctx.author.id)


def setup(client):
    client.add_cog(Thx(client))
