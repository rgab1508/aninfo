import os
from discord.ext import commands
from discord import Embed, Color

from api.api import get_media_by_name, get_media_by_id, get_character_by_name, get_character_by_id, get_studio_by_name, get_studio_by_id



DISCORD_API_TOKEN = os.getenv('ANINFO_DIS_API_TOKEN')
COMMAND_PREFIX = os.getenv('ANINFO_COMMAND_PREFIX') or ","
bot = commands.Bot(command_prefix=COMMAND_PREFIX)


def truncate(txt, l, url=None):
    if l <= len(txt):
        return txt
    else:
        s = txt[:l]
        if url:
            s += f"[.....]({url})"
        else:
            s += "......"
        return s


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
    title = f'[{data["title"]["english"]}]({data["siteUrl"]})'
    em = Embed(title=title, color=Color(0xE5E242))
    em.set_image(url=data['bannerImage'])
    em.set_author(name=data['type'])
    des = truncate(data['description'], 350, url=data['siteUrl'])
    em.add_field(name="Description:", value=des)
    em.add_field(name="Status:", value=data['status'], inline=True)
    em.add_field(name="Format/Duration:", value=f"{data['format']} / {data['duration']} mins")
    s_e = "Yet Not Released" if data['startDate']['day'] is None else f"{data['startDate']['day']}/{data['startDate']['month']}/{data['startDate']['year']}"
    s_e += " - "
    s_e += "None" if data['startDate']['day'] is None else ""
    s_e += "Ongoing" if data['endDate']['day'] is None else ""
    s_e += f"{data['endDate']['day']}/{data['endDate']['month']}/{data['endDate']['year']}" if data['endDate']['day'] else ""
    em.add_field(name="Start/End:", value=s_e)
    em.add_field(name="Episodes: ", value=data['episodes'])
    em.add_field(name="Genres:", value=truncate(", ".join(data['genres']), 35))
    em.add_field(name="Average Score:", value=f"{data['averageScore']}%")
    em.add_field(name="Favourites: ", value=f"{data['favourites']} liked this")
    e_plus = "Yes" if data['isAdult'] == "true" else "No"
    em.add_field(name="18+ :", value=e_plus)
    st = []
    for i in data['studios']['nodes']:
        st.append(i['name'])
    st = " ,".join(st)
    em.add_field(name="Studios:", value=truncate(st, 50))
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
