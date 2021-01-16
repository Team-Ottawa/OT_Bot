import discord
from discord.ext import commands
from PIL import Image
from io import BytesIO
from PIL import ImageFont, ImageDraw, ImageOps
import os
import arabic_reshaper

class welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.client.get_channel(781903031552835655)  # get channel

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


def setup(client):
    client.add_cog(welcome(client))
