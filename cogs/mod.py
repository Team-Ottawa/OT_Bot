import discord
from discord.ext import commands
import db
import config
from datetime import datetime
from discord_ui.cogs import slash_cog


class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @slash_cog(
        name="acceptcode",
        description="accept code to post from codes channel",
        guild_ids=[config.guild_id]
    )
    async def add_code(self, ctx, code_id: str):
        if not ctx.author.guild_permissions.administrator:
            await ctx.respond("You don't have permission administrator", hidden=True)
            return
        x = db.DatabaseCodes(self.client, code_id)
        data = x.info
        if not data:
            await ctx.respond('حمبي هاذ الكود مش موجود, لا توجع لي راسي خذ 🥕')
            return
        embed = discord.Embed(
            title=f'code id: {data.get("_id")}',
            description=f"""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
```{data.get("type")}\n{data.get("code")}\n```
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
{self.client.get_emoji(861366683602911232)} **Title** : {data.get("title")}
{self.client.get_emoji(861366683381923850)} **Description** : {data.get("description")}
{self.client.get_emoji(861366683426619402)} **shared By** : {await self.client.fetch_user(data.get("author_id"))}
{self.client.get_emoji(861366683057651722)} **copyrights** : {data.get("copyrights")}
{self.client.get_emoji(861366681762267157)} **language** : {data.get("type")}
⏳ **Add At:** {datetime.fromtimestamp(data.get("data")).strftime("%m/%d/%Y, %H:%M:%S")}
**[Pastebin]({data.get("link")}) | [Discord](https://discord.gg/ottawa) | [Programming](https://discord.com/channels/@me/{data.get("author_id")})**
""")
        channel = 0
        type_ = data.get("type")
        if type_ == 'python':
            channel = self.client.get_channel(843870818483175436)
        elif type_ == 'javascript':
            channel = self.client.get_channel(843870791262666752)
        try:
            msg = await channel.send("<@&844146353654595584>", embed=embed)
        except discord.errors.HTTPException:
            embed = discord.Embed(
                title=f'code id: {data.get("_id")}',
                description=f"""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
{data.get("link")}\n
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
{self.client.get_emoji(861366683602911232)} **Title** : {data.get("title")}
{self.client.get_emoji(861366683381923850)} **Description** : {data.get("description")}
{self.client.get_emoji(861366683426619402)} **shared By** : {await self.client.fetch_user(data.get("author_id"))}
{self.client.get_emoji(861366683057651722)} **copyrights** : {data.get("copyrights")}
{self.client.get_emoji(861366681762267157)} **language** : {data.get("type")}
⏳ **Add At:** {datetime.fromtimestamp(data.get("data")).strftime("%m/%d/%Y, %H:%M:%S")}
**[Pastebin]({data.get("link")}) | [Discord](https://discord.gg/ottawa) | [Programming](https://discord.com/channels/@me/{data.get("author_id")})**
""")
            msg = await channel.send("<@&844146353654595584>", embed=embed)

        await msg.add_reaction(str(self.client.get_emoji(861371772552347678)))
        await msg.add_reaction(str(self.client.get_emoji(861371772698886164)))
        await channel.send(
            'https://media.discordapp.net/attachments/838138628365353011/855793015384834048/OTTAWA-Codes.gif')
        await ctx.respond('تم نشر الكود في {}'.format(channel.mention))


def setup(client):
    client.add_cog(Mod(client))
