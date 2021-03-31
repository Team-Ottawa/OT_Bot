import discord
from discord.ext import commands
import db


class Xp(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None:
            return
        if message.author.bot:
            return
        db.cr.execute("UPDATE users SET xp = ? WHERE user_id = ?", (db.get_xp(message.author)+1, message.author.id))
        db.db.commit()
        if db.get_xp(message.author) == 500:
            await message.channel.send(f"GG {message.author.mention}, your just send `500` messages ✨.")
            await message.author.add_roles(discord.utils.get(message.author.guild.roles, name="500 messages"))
            return
        elif db.get_xp(message.author) == 1000:
            await message.channel.send(f"GG {message.author.mention}, your just send `1000` messages ✨.")
            await message.author.add_roles(discord.utils.get(message.author.guild.roles, name="1000 messages"))
            return
        elif db.get_xp(message.author) == 2500:
            await message.channel.send(f"GG {message.author.mention}, your just send `2500` messages ✨.")
            await message.author.add_roles(discord.utils.get(message.author.guild.roles, name="2500 messages"))
            return
        elif db.get_xp(message.author) == 5000:
            await message.channel.send(f"GG {message.author.mention}, your just send `5000` messages its hack pro!! ✨.")
            await message.author.add_roles(discord.utils.get(message.author.guild.roles, name="5000 messages"))
            return
        elif db.get_xp(message.author) == 10000:
            await message.channel.send(f"GG {message.author.mention}, your just send `10000` messages your is fire!! 🔥.")
            await message.author.add_roles(discord.utils.get(message.author.guild.roles, name="5000 messages"))
            return


def setup(client):
    client.add_cog(Xp(client))

