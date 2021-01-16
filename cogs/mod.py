import discord
from discord.ext import commands
import json

with open('./config.json', 'r') as f:
    config = json.load(f)


class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
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


def setup(client):
    client.add_cog(Mod(client))
