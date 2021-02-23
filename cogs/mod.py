import discord
from discord.ext import commands
import json

with open('./config.json', 'r') as f:
    config = json.load(f)


class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, ctx):
        channel = self.client.get_channel(813846326017785917)
        if ctx.channel.id != 813842554683785228:
            return
        if ctx.author.bot:
            return
        await channel.send(embed=discord.Embed(
            description=ctx.content,
            color=ctx.author.color
        ).set_footer(text=f"Request by: {ctx.author}").set_thumbnail(url=ctx.author.avatar_url))
        await ctx.delete()

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def accept(self, ctx, member: discord.Member):
        await ctx.send(embed=discord.Embed(
            description="✅ Done been accepted successfully",
            color=0x03ff74
        ))
        # await member.add_roles(discord.utils.get(member.guild.roles, name="Helperᵒᵗ"))
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
                description="❌ Please put the member ID or the mention, and add reason",
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
            description=arg,
            color=discord.Color.red()
        )

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Mod(client))
