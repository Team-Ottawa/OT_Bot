import discord
from discord.ext import commands, tasks
import json
from prettytable import PrettyTable
import asyncio
from PIL import Image
from io import BytesIO
from PIL import ImageFont, ImageDraw, ImageOps
import os
import arabic_reshaper


with open('./config.json', 'r') as f:
    config = json.load(f)

EXTENSIONS = [
    "general",
    "post",
    "submit",
    "mod",
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

    async def on_member_join(self, member):
        channel = self.get_channel(804724196689182740)  # get channel

        img = Image.open("./img/welcome.png")
        ava = member.avatar_url_as(size=128)  # resize avatar member
        data = BytesIO(await ava.read())
        pfp = Image.open(data)

        pfp = pfp.resize((160, 160))
        bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
        mask = Image.new('L', bigsize, 0)

        img.paste(pfp, (905, 30))  # None

        draw = ImageDraw.Draw(mask)

        draw.ellipse((0, 0) + bigsize, fill=255)

        mask = mask.resize(pfp.size, Image.ANTIALIAS)

        pfp.putalpha(mask)

        output = ImageOps.fit(pfp, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        output.save('./img/output.png')
        background = Image.open('./img/welcome.png')
        draw = ImageDraw.Draw(background)
        background.paste(pfp, (45, 90), pfp)
        user_tag = "#" + member.discriminator  # get user tag
        font = ImageFont.truetype("./fonts/Sukar_Black.ttf", size=28)  # font all text
        shadow_color = 0xe6e6e6  # shadow color all text
        stroke_width = 2  # stroke width
        color_stroke = "black"  # color stroke
        draw.text(
            [251, 150],
            arabic_reshaper.reshape(member.name) + user_tag,  # add arabic
            font=font,
            # fill=shadow_color,
            stroke_width=stroke_width,
            stroke_fill=color_stroke)

        background.save('./img/overlap.png')
        await channel.send(
            f"Welcome To OTTAWA: {member.mention}\nrules : <#781902561333870623>",
            file=discord.File("./img/overlap.png"))
        os.remove("./img/output.png")
        os.remove("./img/overlap.png")

    def run(self):
        super().run(self.token, reconnect=True)


if __name__ == '__main__':
    client = sumbot()
    client.run()
