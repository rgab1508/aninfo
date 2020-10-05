import os
from discord.ext import commands
from discord import Embed, Color

from api.api import get_media_by_name, get_media_by_id, get_character_by_name, get_character_by_id, get_studio_by_name, get_studio_by_id



DISCORD_API_TOKEN = os.getenv('ANINFO_DIS_API_TOKEN')
COMMAND_PREFIX = os.getenv('ANINFO_COMMAND_PREFIX') or ","
bot = commands.Bot(command_prefix=COMMAND_PREFIX)


async def searching(ctx, name):
    res = f'{ctx.message.author} searching for "{name}"'
    await ctx.send(res)


@bot.listen()
async def on_ready():
    print("Bot Botting")

@bot.command()
async def search(ctx, *args):
    name = ' '.join(args)
    res = get_media_by_name(name, "ANIME")
    await searching(ctx, name)
    data = res['data']['Media']
    print(data, type(data), data.keys())
    em = Embed(title=data['title']['english'], color=Color(0xE5E242))
    em.set_image(url=data['bannerImage'])
    await ctx.send(embed=em)

@bot.command()
async def charcter(ctx, *args):
    name = ' '.join(args)
    res = get_character_by_name(name)
    await searching(ctx, name)
    print(res)


@bot.command()
async def studio(ctx, *args):
    name = ' '.join(args)
    await searching(ctx, name)
    res = get_studio_by_name(name)
    print(res)

bot.run(DISCORD_API_TOKEN)
