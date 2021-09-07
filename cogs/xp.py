import discord
from discord.ext import commands, tasks
import db
import config
from discord_ui.cogs import slash_cog, subslash_cog


class Xp(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None:
            return
        if message.author.bot:
            return
        x = db.DatabaseUsers(self.client, message.author.id)
        x.update_xp()
        user_xp = x.info.get("xp")
        if user_xp == 25:
            await message.channel.send(f"GG {message.author.mention}, your just send `25` messages ✨.")
            return
        elif user_xp == 50:
            await message.channel.send(f"GG {message.author.mention}, your just send `50` messages ✨.")
            return
        elif user_xp == 100:
            await message.channel.send(f"GG {message.author.mention}, your just send `100` messages ✨.")
            return
        elif user_xp == 250:
            await message.channel.send(f"GG {message.author.mention}, your just send `250` messages ✨.")
            return
        elif user_xp == 500:
            await message.channel.send(f"GG {message.author.mention}, your just send `500` messages ✨.")
            await message.author.add_roles(discord.utils.get(message.author.guild.roles, name="500 messages"))
            return
        elif user_xp == 1000:
            await message.channel.send(f"GG {message.author.mention}, your just send `1000` messages ✨.")
            await message.author.add_roles(discord.utils.get(message.author.guild.roles, name="1000 messages"))
            return
        elif user_xp == 2500:
            await message.channel.send(f"GG {message.author.mention}, your just send `2500` messages ✨.")
            await message.author.add_roles(discord.utils.get(message.author.guild.roles, name="2500 messages"))
            return
        elif user_xp == 5000:
            await message.channel.send(f"GG {message.author.mention}, your just send `5000` messages its hack pro!! ✨.")
            await message.author.add_roles(discord.utils.get(message.author.guild.roles, name="5000 messages"))
            return
        elif user_xp == 10000:
            await message.channel.send(f"GG {message.author.mention}, your just send `10000` messages your is fire!! 🔥.")
            await message.author.add_roles(discord.utils.get(message.author.guild.roles, name="5000 messages"))
            return

    @tasks.loop(minutes=1)
    async def voice_xp(self):
        guild = self.client.get_guild(config.guild_id)
        for channel in guild.voice_channels:
            for member in channel.members:
                if member.bot:
                    continue
                _id = member.id
                x = db.DatabaseUsers(self.client, _id)
                _info = x.info
                x.update_where("voice_xp", _info.get("voice_xp")+2)

    @commands.Cog.listener()
    async def on_ready(self):
        self.voice_xp.start()

    @slash_cog(
        name="leaderboard",
        guild_ids=[config.guild_id],
        description="Get leaderboards from the server",
    )
    async def top(self, ctx):
        msg = await ctx.respond("شكرا لانك واحد محترم تستعمل بوت اوتاوا الاصلي انتظر شوي اذا تقدر")
        top_xp = ""
        top_thanks = ""
        top_voice = ""
        x = db.DatabaseUsers(self.client, ctx.author.id)
        for z, i in enumerate(x.top_xp(count=5)):
            if i.get("_id") == ctx.author.id:
                top_xp += "**#%s | <@%s> XP: `%s`**\n" % (
                    i.get("num"),
                    i.get('_id'),
                    i.get("xp")
                )
                continue
            top_xp += "#%s | <@%s> XP: `%s`\n" % (
                i.get("num"),
                i.get('_id'),
                i.get("xp")
            )
        for z, i in enumerate(x.top_thanks(count=5)):
            if i.get("_id") == ctx.author.id:
                top_thanks += "**#%s | <@%s> XP: `%s`**\n" % (
                    i.get("num"),
                    i.get('_id'),
                    i.get("thanks")
                )
                continue
            top_thanks += "#%s | <@%s> XP: `%s`\n" % (
                i.get("num"),
                i.get('_id'),
                i.get("thanks")
            )
        for z, i in enumerate(x.top_voice(count=5)):
            if i.get("_id") == ctx.author.id:
                top_voice += "**#%s |** <@%s> XP: `%s`\n" % (
                    i.get("num"),
                    i.get('_id'),
                    i.get("voice_xp")
                )
                continue
            top_voice += "#%s | <@%s> XP: `%s`\n" % (
                i.get("num"),
                i.get('_id'),
                i.get("voice_xp")
            )
        embed = discord.Embed(
            title="Ottawa Top Leaderboards",
            color=0xFFFDFD
        )
        embed.add_field(name='💬 top xp', value=top_xp + "✨ More? `/top xp`", inline=True)
        embed.add_field(name='🌟 top thanks', value=top_thanks + "✨ More? `/top thanks`", inline=True)
        embed.add_field(name='🔊 top voice', value=top_voice + "✨ More? `/top voice`", inline=False)
        await msg.edit(content="_ _", embed=embed)

    @subslash_cog(
        base_names="top",
        name="voice",
        guild_ids=[config.guild_id],
        description="Get voice leaderboards from the server",
    )
    async def top_voice(self, ctx, page_id: int = 1):
        msg = await ctx.respond("شكرا لانك واحد محترم تستعمل بوت اوتاوا الاصلي انتظر شوي اذا تقدر")
        x = db.DatabaseUsers(self.client, ctx.author.id)
        v = x.get_from_page_id(module='voice_xp', page_id=page_id)
        top_voice = ""
        for z, i in enumerate(v):
            if i.get("_id") == ctx.author.id:
                top_voice += "**#%s | <@%s> XP: `%s`**\n" % (
                    i.get("num"),
                    i.get('_id'),
                    i.get("voice_xp")
                )
                continue
            top_voice += "#%s | <@%s> XP: `%s`\n" % (
                i.get("num"),
                i.get('_id'),
                i.get("voice_xp")
            )
        embed = discord.Embed(
            title="Ottawa Top Voice Leaderboards",
            color=0xFFFDFD
        )
        embed.add_field(name='🔊 top voice [%s/%s]' % (page_id, round(len([i for i in x.all]) / 10)), value=top_voice, inline=True)
        await msg.edit(content="_ _", embed=embed)

    @subslash_cog(
        base_names="top",
        name="xp",
        guild_ids=[config.guild_id],
        description="Get messages leaderboards from the server",
    )
    async def top_text(self, ctx, page_id: int = 1):
        msg = await ctx.respond("شكرا لانك واحد محترم تستعمل بوت اوتاوا الاصلي انتظر شوي اذا تقدر")
        top_xp = ""
        x = db.DatabaseUsers(self.client, ctx.author.id)
        v = x.get_from_page_id(module='xp', page_id=page_id)
        for z, i in enumerate(v):
            if i.get("_id") == ctx.author.id:
                top_xp += "**#%s | <@%s> XP: `%s`**\n" % (
                    i.get("num"),
                    i.get('_id'),
                    i.get("xp")
                )
                continue
            top_xp += "#%s | <@%s> XP: `%s`\n" % (
                i.get("num"),
                i.get('_id'),
                i.get("xp")
            )
        embed = discord.Embed(
            title="Ottawa Top Text Leaderboards",
            color=0xFFFDFD
        )
        embed.add_field(name='💬 top xp [%s/%s]' % (page_id, round(len([i for i in x.all]) / 10)), value=top_xp, inline=True)
        await msg.edit(content="_ _", embed=embed)

    @subslash_cog(
        base_names="top",
        name="thanks",
        guild_ids=[config.guild_id],
        description="Get thanks leaderboards from the server",
    )
    async def top_thanks(self, ctx, page_id: int = 1):
        msg = await ctx.respond("شكرا لانك واحد محترم تستعمل بوت اوتاوا الاصلي انتظر شوي اذا تقدر")
        top_thanks = ""
        x = db.DatabaseUsers(self.client, ctx.author.id)
        v = x.get_from_page_id(module='thanks', page_id=page_id)
        for z, i in enumerate(v):
            if i.get("_id") == ctx.author.id:
                top_thanks += "**#%s | <@%s> XP: `%s`**\n" % (
                    i.get("num"),
                    i.get('_id'),
                    i.get("thanks")
                )
                continue
            top_thanks += "#%s | <@%s> XP: `%s`\n" % (
                i.get("num"),
                i.get('_id'),
                i.get("thanks")
            )
        embed = discord.Embed(
            title="Ottawa Top Thanks Leaderboards",
            color=0xFFFDFD
        )
        embed.add_field(
            name='🌟 top thanks [%s/%s]' % (page_id, round(len([i for i in x.all]) / 10)),
            value=top_thanks, inline=True
        )
        await msg.edit(content="_ _", embed=embed)


def setup(client):
    client.add_cog(Xp(client))

