import discord
import requests
import urllib.parse
import os

from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TRACE_MOE_URL = os.getenv('TRACE_MOE_URL')

bot = commands.Bot(command_prefix='!')


def download_video(url: str):
    response = requests.get(url)
    now_timestamp = int(datetime.now().timestamp())
    open('temp/' + str(now_timestamp) + '.mp4', 'wb').write(response.content)
    return 'temp/' + str(now_timestamp) + '.mp4'


def delete_file(file: str):
    if os.path.exists(file):
        os.remove(file)


def get_anime(url: str):
    result = requests.get("{}?cutBorders&url={}".format(TRACE_MOE_URL, urllib.parse.quote_plus(url))).json() \
        .get('result')

    anime_info = result[0]
    video = download_video(anime_info['video'])

    anime = "Anime : `{}`\nEpisode : {}\nTimestamp : {} - {}" \
        .format(anime_info['filename'], anime_info['episode'], int(anime_info['from']), int(anime_info['to']))

    return [anime, video]


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='tracturl', help='Find out an anime by sending a url using <!tract @image_url>')
async def tracturl(ctx, image_url: str):
    anime = get_anime(image_url)
    await ctx.send(anime[0], file=discord.File(anime[1]))
    delete_file(anime[1])


@bot.command(name='tractimage', help='Find out an anime by sending a capture using <!tract @attachment>')
async def tractimage(ctx):
    message = ctx.message
    if message.attachments:
        image_url = message.attachments[0].url
        anime = get_anime(image_url)
        await ctx.send(anime[0], file=discord.File(anime[1]))
        delete_file(anime[1])
    else:
        await ctx.send("You need to send an image")


bot.run(TOKEN)
