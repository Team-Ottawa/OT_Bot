import discord
from discord.ext import commands, tasks
import os
import json
from prettytable import PrettyTable
import asyncio


replay = {
    ".": "اهلان بيك منورنا السيرفر يا غالي",
}

with open('./config.json', 'r') as f:
    config = json.load(f)

EXTENSIONS = [
    "general",
    "post",
    "submit",
    "mod",
    "welcome"
]


class sumbot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=config["prefix"],
            case_insensitive=True,
            allowed_mentions=discord.AllowedMentions(
                everyone=config["mention"]["everyone"],
                users=config["mention"]["users"],
                roles=config["mention"]["roles"]),
            intents=discord.Intents.all()
)
        self.client_id = config["client_id"]
        self.owner_id = config["owner_id"]

        if config["token"] == "" or config["token"] == "token":
            self.token = os.environ['token']
        else:
            self.token = config["token"]

        for filename in EXTENSIONS:
            # try:
                self.load_extension(f'cogs.{filename}')
                # print('lode {}'.format(filename))
            # except:
            #     print('error in {}'.format(filename))

    @tasks.loop(seconds=10.0)
    async def change_stats(self):

        status = [
            '{0}help | OT Bot'.format(self.command_prefix),
            'OTTAWA Team Is Best'
            ]
        await self.change_presence(activity=discord.Game(type=discord.ActivityType.listening, name=(status[0])))
        await asyncio.sleep(30)
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status[1]))
        await asyncio.sleep(10)

    async def on_ready(self):
        self.change_stats.start()
        tap = PrettyTable(
            ['Name Bot', 'Id', 'prefix', 'commands', 'users'])
        tap.add_row([
            self.user.display_name,
            str(self.user.id),
            self.command_prefix,
            len(self.commands),
            len(self.users),
        ])
        print(tap)

    # async def on_message(self, ctx):
    #     if ctx.content in replay:
    #         await ctx.channel.send(replay[ctx.content])
    #     else:
    #         pass

    def run(self):
        super().run(self.token, reconnect=True)


if __name__ == '__main__':
    client = sumbot()
    client.run()