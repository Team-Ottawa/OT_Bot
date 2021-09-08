import discord
from discord.ext import commands
from discord_ui.cogs import slash_cog
from discord_ui.receive import SlashedCommand
from requests import request
import config
from bs4 import BeautifulSoup


class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_cog(
        name="pypi",
        description="Search to python projects from pypi.org",
        guild_ids=[config.guild_id]
    )
    async def pypi(self, ctx: SlashedCommand, project_name: str):
        re = request(
            "GET",
            f"https://pypi.org/pypi/{project_name}/json",

        )
        data: dict = re.json()["info"]
        description = data["description"]
        if len(description) >= 1000:
            description = description[:1000] + f"..."
        embed = discord.Embed(
            title=data.get("name"),
            url=data.get("package_url"),
            description=f'```md\n{description}\n```',
            color=discord.Color.random()
        )
        embed.add_field(name="Author", value=data.get("author"))
        embed.add_field(name="Documentation", value=data.get("project_urls").get("Documentation"))
        embed.add_field(name="Github", value=data.get("project_urls").get("Homepage"))
        embed.add_field(name="releases length", value=str(len(re.json().get("releases"))))
        await ctx.respond(embed=embed)

    @slash_cog(
        name="npm",
        description="Search to nodejs package from npmjs.com",
        guild_ids=[config.guild_id]
    )
    async def npm(self, ctx: SlashedCommand, package_name: str):
        re = request(
            "GET",
            f"https://www.npmjs.com/package/{package_name}",
            headers={
                "content-type": "application/json"
            }
        )
        soup = BeautifulSoup(re.content, "lxml")
        data = {
            "Repository": soup.find("a", {"aria-labelledby": "repository"}).get("href"),
            "Homepage": soup.find("a", {"aria-labelledby": "homePage"}).get("href"),
            "WeeklyDownloads": soup.find("p", {"class": "_9ba9a726 f4 tl flex-auto fw6 black-80 ma0 pr2 pb1"}).text,
            "version": soup.find("p", {"class": "f2874b88 fw6 mb3 mt2 truncate black-80 f4"}).text,
            "License": soup.findAll("p", {"class": "f2874b88 fw6 mb3 mt2 truncate black-80 f4"})[1].text,
            "Last publish": soup.findAll("time")[1].text
        }

        embed = discord.Embed(
            title=package_name,
            url=re.url,
            color=discord.Color.random()
        )
        for name, value in data.items():
            embed.add_field(name=name, value=value)
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Search(bot))

