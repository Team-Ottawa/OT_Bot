import discord
from discord.ext import commands
import json
import db


with open('./config.json', 'r') as f:
    config = json.load(f)


class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    # @commands.command(hidden=True)
    # @commands.guild_only()
    # @commands.has_permissions(administrator=True)
    # async def accept(self, ctx, member: discord.Member):
    #     await ctx.send(embed=discord.Embed(
    #         description="✅ Done been accepted successfully",
    #         color=0x03ff74
    #     ))
    #     # await member.add_roles(discord.utils.get(member.guild.roles, name="Helperᵒᵗ"))
    #     await member.send(embed=discord.Embed(
    #         description="✅ You have been accepted successfully",
    #         color=0x03ff74
    #     ))
    #
    # @commands.command(hidden=True)
    # @commands.guild_only()
    # @commands.has_permissions(administrator=True)
    # async def reject(self, ctx, member: discord.Member, *, reason):
    #     await ctx.send(embed=discord.Embed(
    #         description=f"✅ Done been Unfortunately for {member.mention}",
    #         color=0x03ff74
    #     ))
    #     await member.send(embed=discord.Embed(
    #         description=f"❌ You have Unfortunately, you were rejected because of:\n{reason}\nIf you have any objections, please contact {ctx.author}",
    #         color=0xf7072b
    #     ))

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

    @commands.command(name='add', aliases=["acceptcode", "addcode"], hidden=True)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def add_code(self, ctx, code_id):
        x = db.DatabaseCodes(self.client, code_id)
        data = x.info
        if data is None:
            await ctx.send('حمبي هاذ الكود مش موجود, لا توجع لي راسي خذ 🥕')
            return
        embed = discord.Embed(
            title=f'code id: {data.get("_id")}',
            description=f"""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
```{data.get("type")[:2]}\n{data.get("code")}\n```
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
{self.client.get_emoji(761876595770130452)} **Title** : {data.get("title")}
{self.client.get_emoji(761876609358757918)} **Description** : {data.get("description")}
{self.client.get_emoji(761876608196804609)} **shared By** : {await self.client.fetch_user(data.get("author_id"))}
{self.client.get_emoji(761876614761807883)} **copyrights** : {data.get("copyrights")}
{self.client.get_emoji(761876595006767104)} **language** : {data.get("type")}
⏳ **Add At:** {data.get("data")}
**[Pastebin]({data.get("link")}) | [Discord](https://discord.gg/sUZ2W8FDKr) | [Programming](https://discord.com/channels/@me/{data.get("author_id")})**
""")
        channel = 0
        type_ = data.get("type")
        if type_ == 'python':
            channel = self.client.get_channel(781915117033357332)
        elif type_ == 'javascript':
            channel = self.client.get_channel(827135291570782248)
        elif type_ == 'html':
            channel = self.client.get_channel(814087413122072596)
        msg = await channel.send("<@&813514248142717011>", embed=embed)
        await msg.add_reaction(str(self.client.get_emoji(815537841319706654)))
        await msg.add_reaction(str(self.client.get_emoji(815537927462453258)))
        await channel.send('https://cdn.discordapp.com/attachments/804403574712565781/835966184997781544/42_E25EB2C-1.gif')
        await ctx.send('تم نشر الكود في {}'.format(channel.mention))


def setup(client):
    client.add_cog(Mod(client))
