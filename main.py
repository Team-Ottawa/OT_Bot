import discord
from discord.ext import commands, tasks
import json
from prettytable import PrettyTable
import asyncio
import os
import db


with open('./config.json', 'r') as f:
    config = json.load(f)

EXTENSIONS = [
    "general",
    "post",
    # "submit",
    "mod",
    "welcome",
    # "verified",
    "thx",
    "errors",
    "help",
    "xp",
    "vip",
    # 'dlel'
]


client = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    case_insensitive=True,
    allowed_mentions=discord.AllowedMentions(
        everyone=config["mention"]["everyone"],
        users=config["mention"]["users"],
        roles=config["mention"]["roles"]),
    intents=discord.Intents.all()
)
client.remove_command('help')
client.client_id = config["client_id"]
client.owner_ids = config["owner_id"]

if config["token"] == "" or config["token"] == "token":
    client.token = os.environ['token']
else:
    client.token = config["token"]

for filename in EXTENSIONS:
    try:
        client.load_extension(f'cogs.{filename}')
        print('lode {}'.format(filename))
    except:
        print('error in {}'.format(filename))


@tasks.loop(seconds=10.0)
async def change_stats():
    status = [
        '!help | OTTAWA.exe',
        'OTTAWA Team',
        '🧀'
        ]
    await client.change_presence(activity=discord.Game(type=discord.ActivityType.listening, name=(status[0])))
    await asyncio.sleep(30)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status[1]))
    await asyncio.sleep(10)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status[2]))
    await asyncio.sleep(10)


@client.event
async def on_ready():
    change_stats.start()
    tap = PrettyTable(
        ['Name Bot', 'Id', 'prefix', 'commands', 'users'])
    tap.add_row([
        client.user.display_name,
        str(client.user.id),
        "!",
        len(client.commands),
        len(client.users),
    ])
    print(tap)


if __name__ == '__main__':
    client.run(client.token, reconnect=True)
