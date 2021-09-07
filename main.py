import discord
from discord.ext import commands
import config
from prettytable import PrettyTable
import os
import DiscordUtils
from discord_ui import UI


cogs = [
    "general",
    "post",
    "youtube",
    "mod",
    "welcome",
    "license",
    "thx",
    "errors",
    "help",
    "xp",
]


def get_prefix(bot, msg):
    return commands.when_mentioned_or(config.prefix)(bot, msg)


client = commands.Bot(
    command_prefix=get_prefix,
    case_insensitive=True,
    allowed_mentions=discord.AllowedMentions(
        everyone=False,
        users=True,
        roles=False
    ),
    intents=discord.Intents.all(),
    owner_ids=config.owner_ids
)

ui = UI(client)
client.tracker = DiscordUtils.InviteTracker(client)
client.remove_command('help')


if config.token == "" or config.token == "token":
    client.token = os.environ['token']
else:
    client.token = config.token

for filename in cogs:
    try:
        client.load_extension(f'cogs.{filename}')
        print('lode {}'.format(filename))
    except Exception as error:
        print('error in {} as [{}]'.format(filename, error))


@client.event
async def on_invite_create(invite):
    await client.tracker.update_invite_cache(invite)


@client.event
async def on_invite_delete(invite):
    await client.tracker.remove_invite_cache(invite)


@client.event
async def on_ready():
    await client.tracker.cache_invites()
    # for i in client.users:
    #     z = db.Coins(client, i.id)
    #     z.insert()
    #     x = db.DatabaseUsers(client, i.id)
    #     if i.bot:
    #         continue
    #     x.insert()
    await client.change_presence(
        activity=discord.Activity(name='%shelp - discord.gg/ottawa' % config.prefix, type=discord.ActivityType.playing),
        status=discord.Status.dnd
    )
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
