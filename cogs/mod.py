import discord
from discord.ext import commands
import json
import db


with open('./config.json', 'r') as f:
    config = json.load(f)


class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(hidden=True)
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

    @commands.command(hidden=True)
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

    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def say(self, ctx, *, arg):
        await ctx.message.delete()
        await ctx.send(arg)

    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def embed(self, ctx, *, arg):
        await ctx.message.delete()
        embed = discord.Embed(
            description=arg,
            color=discord.Color.red()
        )

        await ctx.send(embed=embed)

    @commands.command(name='add', aliases=["acceptcode", "addcode"])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def add_code(self, ctx, code_id):
        date = db.get_code(code_id)
        embed = discord.Embed(
            title=f'code id: {date[0]}',
            description=f"""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
```{date[3][:2]}\n{date[6]}\n```
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
{self.client.get_emoji(761876595770130452)} **Title** : {date[1]}
{self.client.get_emoji(761876609358757918)} **Description** : {date[2]}
{self.client.get_emoji(761876608196804609)} **shared By** : {date[4]}
{self.client.get_emoji(761876614761807883)} **copyrights** : {date[5]}
{self.client.get_emoji(761876595006767104)} **language** : {date[3]}           
""")
        channel = 0
        if date[3] == 'python':
            channel = self.client.get_channel(781915117033357332)
        elif date[3] == 'javascript':
            channel = self.client.get_channel(827135291570782248)
        elif date[3] == 'html':
            channel = self.client.get_channel(814087413122072596)
        await channel.send("<@&813514248142717011>", embed=embed, allowed_mentions=discord.AllowedMentions.none())
        await ctx.send('تم نشر الكود في {}'.format(channel.mention))


def setup(client):
    client.add_cog(Mod(client))
