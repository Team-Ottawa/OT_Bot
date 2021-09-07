from discord.ext import commands
import config
from discord_ui.cogs import slash_cog


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @slash_cog(
        name="help",
        guild_ids=[config.guild_id],
        description="Show help from all commands"
    )
    async def help_command(self, ctx):
        await ctx.respond("كل الأومر واضحة ما بدها بابا و ماما", hidden=True)


def setup(client):
    client.add_cog(Help(client))

