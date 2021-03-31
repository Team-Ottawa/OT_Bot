import discord
from discord.ext import commands
import db


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="help")
    @commands.guild_only()
    async def help_command(self, ctx, *, command=None):
        # print(self.client.commands)
        if command is not None:
            command = self.client.get_command(command)
            if command is None:
                await ctx.send("❌ I could not find this command")
            str_ = ""
            if command.aliases is not []:
                str_ = f"**aliases:** {', '.join(command.aliases)}"
            await ctx.send(f"**command:** {db.get_prefix(ctx.author)}{command.name} {command.signature}\n{str_}")
            return
        # commands = [i.name for i in self.client.commands]
        # list_commands = self.client.commands
        await ctx.send(embed=discord.Embed(description="\n".join([f"**{db.get_prefix(ctx.author)}{i.name} {i.signature}**" for i in self.client.commands])))

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot:
            return



def setup(client):
    client.add_cog(Help(client))

