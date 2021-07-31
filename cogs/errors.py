import discord
from discord.ext import commands
import config


class ErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

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
                description=f"{config.prefix}{ctx.command.name} {ctx.command.signature}",
                color=discord.Colour.red()
            ).set_author(name=ctx.command.cog_name)
            await ctx.send(embed=embed)
            return
        elif isinstance(error, commands.errors.BadArgument):
            embed = discord.Embed(
                description=f"{config.prefix}{ctx.command.name} {ctx.command.signature}",
                color=discord.Colour.red()
            ).set_author(name=ctx.command.cog_name)
            await ctx.send(embed=embed)
            return
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.send("Missing permissions `%s`" % error.missing_perms)
            return
        elif isinstance(error, commands.errors.BotMissingPermissions):
            await ctx.send("I Missing permissions `%s`" % error.missing_perms)
        elif isinstance(error, commands.errors.CommandNotFound):
            return
        elif isinstance(error, commands.errors.MissingRole):
            await ctx.send("Missing role `%s`" % error.missing_role)
            return
        if isinstance(error, discord.errors.NotFound):
            return
        else:
            await ctx.send(error)


def setup(client):
    client.add_cog(ErrorHandler(client))
