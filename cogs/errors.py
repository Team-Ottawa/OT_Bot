import discord
from discord.ext import commands
import db


class ErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cooldown = []

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            await ctx.send(embed=discord.Embed(
                description=f"This command is currently **on cooldown** for ,Please **try again in** `{'%02d seconds' % (s,)}`.",
                color=discord.Colour.red()
            ),  delete_after=2)
            return
        elif isinstance(ctx.channel, discord.channel.DMChannel):
            return
        elif isinstance(error, commands.errors.MemberNotFound):
            embed = discord.Embed(
                description=f"❌ I could not find this member",
                color=discord.Colour.red()
            )
            await ctx.send(embed=embed)
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                description=f"!{ctx.command.name} {ctx.command.signature}",
                color=discord.Colour.red()
            ).set_author(name=ctx.command.cog_name)
            await ctx.send(embed=embed)
            return
        elif isinstance(error, commands.errors.BadArgument):
            embed = discord.Embed(
                description=f"!{ctx.command.name} {ctx.command.signature}",
                color=discord.Colour.red()
            ).set_author(name=ctx.command.cog_name)
            await ctx.send(embed=embed)
            return
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.send(error)
        else:
            await ctx.send(error)


def setup(client):
    client.add_cog(ErrorHandler(client))
