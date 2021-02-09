import discord
from discord.ext import commands
import json

with open('./config.json', 'r') as f:
    config = json.load(f)


class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def accept(self, ctx, member: discord.Member):
        await ctx.send(embed=discord.Embed(
            description="✅ Done been accepted successfully",
            color=0x03ff74
        ))
        await member.add_roles(discord.utils.get(member.guild.roles, name="Helper"))
        await member.send(embed=discord.Embed(
            description="✅ You have been accepted successfully",
            color=0x03ff74
        ))

    @commands.has_permissions(administrator=True)
    @accept.error
    async def accept_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                description="❌ Please put the member ID or the mention",
                color=0xf7072b
            ))
        if isinstance(error, commands.MissingPermissions):
            pass

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def reject(self, ctx, member: discord.Member, *, reason):
        await ctx.send(embed=discord.Embed(
            description=f"✅ Done been Unfortunately for {member.mention}",
            color=0x03ff74
        ))
        await member.send(embed=discord.Embed(
            description=f"❌ You have Unfortunately, you were rejected because of:\n{reason}\nIf you have any objections, please contact {ctx.author}",
            color=0xf7072b
        ))

    @commands.has_permissions(administrator=True)
    @reject.error
    async def reject_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                description="❌ Please put the member ID or the mention, and add ",
                color=0xf7072b
            ))
        if isinstance(error, commands.MissingPermissions):
            pass

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def say(self, ctx, *, arg):
        await ctx.message.delete()
        await ctx.send(arg)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def embed(self, ctx, *, arg):
        await ctx.message.delete()
        embed = discord.Embed(
            title="OTTAWA Server",
            description=arg,
            timestamp=ctx.message.created_at,
            color=0xff1303)
        embed.set_image(url="https://cdn.discordapp.com/attachments/754398470558842930/771086560941965322/42_E25EB2C-1.gif")
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_author(name=self.client.user, icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Mod(client))
