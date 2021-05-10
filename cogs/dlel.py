import discord
from discord.ext import commands
import db
import requests
from datetime import datetime


def is_url_image(image_url):
   image_formats = ("image/png", "image/jpeg", "image/jpg")
   r = requests.head(image_url)
   if r.headers["content-type"] in image_formats:
      return True
   return False


class Dlel(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='dlel')
    @commands.guild_only()
    async def dlel_(self, ctx, dlel: str = None):

        if dlel is not None:
            attachments = dlel
        try:
            check = is_url_image(attachments)
            if check is False:
                await ctx.send(f'**{dlel}**, this is not img')
                return
            try:
                db.add_dlel(ctx.author, dlel, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                await ctx.send('done successfully add your dlel')
                return
            except db.mysql.connector.errors.IntegrityError:
                await ctx.send('You really send your dlel')
                return
        except requests.exceptions.MissingSchema:
            await ctx.send(f'**{dlel}**, this is not img')
            return
        attachments = ctx.message.attachments
        attachments = attachments[0]
        if attachments is []:
            embed = discord.Embed(
                description=f"{db.get_prefix(ctx.author)}{ctx.command.name} {ctx.command.signature}",
                color=discord.Colour.red()
            ).set_author(name=ctx.command.cog_name)
            await ctx.send(embed=embed)
            return
        # try:
        #     db.add_dlel(ctx.author, str(attachments[0]), datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        #     await ctx.send('done successfully add your dlel')
        # except db.mysql.connector.errors.IntegrityError:
        #     await ctx.send('You really send your dlel')
        #     return

    @commands.command(name='checkdlel')
    @commands.guild_only()
    @commands.is_owner()
    async def check_dlel(self, ctx, user: discord.Member):
        data = db.get_dlel(user)
        if data is None:
            await ctx.send('هاذ شخص كذاب ما سوا الشرط -_-')
            return
        embed = discord.Embed(
            color=discord.Color.green()
        )
        embed.add_field(name='Add at:', value=data[3])
        embed.set_image(url=data[2])
        await ctx.send('{}, كفو عليك انت مسوي الشرط'.format(user.mention), embed=embed)

    @commands.command(name='deletedlel')
    @commands.guild_only()
    @commands.is_owner()
    async def delete_dlel(self, ctx):
        db.delete_all_dlel()
        await ctx.send('حمبي تم حذف كل الادله')


def setup(client):
    client.add_cog(Dlel(client))
