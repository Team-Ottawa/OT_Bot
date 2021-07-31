import discord
from discord.ext import commands
import config


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="help", help='show this message')
    @commands.guild_only()
    async def help_command(self, ctx, *, command=None):
        if command is not None:
            command = self.client.get_command(command)
            if command is None:
                await ctx.send("❌ I could not find this command")
            str_ = ""
            if command.aliases is not []:
                str_ = f"**aliases:** {', '.join(command.aliases)}"
            await ctx.send(f"**command:** {config.prefix}{command.name} {command.signature}\n{str_}")
            return
        list_commands = []
        for i in self.client.commands:
            if i.hidden:
                continue
            list_commands.append(f"**{config.prefix}{i.name} {i.signature}** - {i.help}")
        embed = discord.Embed(description="\n".join(list_commands), color=ctx.author.color)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_image(url="https://cdn.discordapp.com/attachments/770235184477634590/827052493224935454/fe4f45f31647abe2.png")
        embed.set_author(name=self.client.user.display_name + " [✓BOT]", icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Help(client))

