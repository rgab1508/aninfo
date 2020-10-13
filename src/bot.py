import os
import datetime
from discord.ext import commands
from discord import Embed, Color

from api.api import get_media_by_name, get_media_by_id, get_character_by_name, get_character_by_id, get_studio_by_name, get_studio_by_id



DISCORD_API_TOKEN = os.getenv('ANINFO_DIS_API_TOKEN')
COMMAND_PREFIX = os.getenv('ANINFO_COMMAND_PREFIX') or ","
bot = commands.Bot(command_prefix=COMMAND_PREFIX)


def truncate(txt, l, url=None):
    txt = txt.replace("<strong>", "**")
    txt = txt.replace("</strong>", "**")
    txt = txt.replace("<i>", "*")
    txt = txt.replace("</i>", "*")
    txt = txt.replace("~", "|")
    txt = txt.replace("!", "|")
    txt = txt.replace("<br>", "").strip()
    if l > len(txt):
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
    print(res)
    await ctx.send(res)

def get_media_embed(data):
    em = Embed(title=data['title']['english'] or data['title']['romaji'] or data['title']['native'], color=Color.purple())
    if data['bannerImage']:
        em.set_image(url=data['bannerImage'])
    em.set_author(name="id#"+str(data['id']), url=data['siteUrl'])
    des = truncate(data['description'], 400)
    em.add_field(name="Description:", value=des, inline=False)
    em.add_field(name="Status:", value=data['status'])
    if data['type'] == "ANIME":
        em.add_field(name="Format/Duration:", value=f"{data['format']} / {data['duration']} mins")
    s_e = "Yet Not Released" if data['startDate']['day'] is None else f"{data['startDate']['day']}.{data['startDate']['month']}.{data['startDate']['year']}"
    s_e += " - "
    s_e += "None" if data['startDate']['day'] is None else ""
    s_e += "Ongoing" if data['endDate']['day'] is None else ""
    s_e += f"{data['endDate']['day']}.{data['endDate']['month']}.{data['endDate']['year']}" if data['endDate']['day'] else ""
    em.add_field(name="Date(Start-End):", value=s_e, inline=False)
    if data['type'] == "ANIME":
        if data['status'] == "RELEASING":
            at = f"Airing episode {data['nextAiringEpisode']['episode']} At "
            d = datetime.datetime.utcfromtimestamp(data['nextAiringEpisode']['airingAt'])
            d = d.strftime("%d.%m.%Y %H:%MUTC")
            at += d
            em.add_field(name="Episodes:", value=at, inline=False)
        else:
            em.add_field(name="Episodes: ", value=data['episodes'])
    else:
        em.add_field(name="Volumes: ", value=data['volumes'] or "None")
        em.add_field(name="Chapters : ", value=data['chapters'] or "None")
    em.add_field(name="Genres:", value=truncate(", ".join(data['genres']), 70), inline=False)
    em.add_field(name="Favourites: ", value=f"{data['favourites']} anilist users liked this", inline=False)
    em.add_field(name="Average Score:", value=f"{data['averageScore']}%")
    e_plus = "Yes" if data['isAdult'] == "true" else "No"
    em.add_field(name="18+ :", value=e_plus)
    if data['type'] == "ANIME" and len(data['studios']['nodes']) > 0:
        st = []
        for i in data['studios']['nodes']:
            st.append(i['name'])
        st = ", ".join(st)
        em.add_field(name="Studios:", value=truncate(st, 50), inline=False)
    ot = []
    for i in data['title'].keys():
        if data['title'][i]:
            ot.append(data['title'][i])
    ot = ", ".join(ot)
    em.add_field(name="Other Names:", value=ot)
    return em

@bot.listen()
async def on_ready():
    print("Bot Botting")

@bot.command()
async def search(ctx, *args):
    name = ' '.join(args)
    res = get_media_by_name(name, "ANIME")
    await searching(ctx, name)
    data = res['data']['Media']
    if data is None:
        await ctx.send("Can't Find the anime you are looking for :(")
        return
    print(data)
    em = get_media_embed(data)
    await ctx.send(embed=em)

@bot.command()
async def searchm(ctx, *args):
    name = ' '.join(args)
    res = get_media_by_name(name, "MANGA")
    await searching(ctx, name)
    data = res['data']['Media']
    if data is None:
        await ctx.send("Can't Find the manga you are looking for :(")
        return
    em = get_media_embed(data)
    await ctx.send(embed=em)

@bot.command()
async def character(ctx, *args):
    name = ' '.join(args)
    await searching(ctx, name)
    res = get_character_by_name(name)
    data = res['data']['Character']
    if data is None:
        await ctx.send("Cant Find the character you are looking for :(")
        return
    print(data, data.keys())
    em = Embed(title=data['name']['full'])
    em.set_thumbnail(url=data['image']['medium'])
    if data['description']:
        des = truncate(data['description'], 1000)
        des = des.replace("__", "**")
        em.add_field(name="Description: ", value=des, inline=False)
    em.add_field(name="Favourites: ", value=f"{data['favourites']} Anilist users liked this character", inline=False)
    f_list = []
    m_list = []
    for i in sorted(data['media']['nodes'], key=lambda x: x['favourites'], reverse=True):
        title = i['title']
        fmt = i['format']
        if fmt == "MOVIE":
            m_list.append(title['english'] or title['romaji'] or title['native'])
        else:
            f_list.append(title['english'] or title['romaji'] or title['native'])
    f_list = '\n'.join(f_list[:5])
    m_list = '\n'.join(m_list[:5])
    if len(f_list) > 0:
        em.add_field(name="From: ", value=f_list, inline=False)
    if len(m_list) > 0:
        em.add_field(name="Movies:", value=m_list, inline=False)
    await ctx.send(embed=em)

@bot.command()
async def studio(ctx, *args):
    name = ' '.join(args)
    await searching(ctx, name)
    res = get_studio_by_name(name)
    data = res['data']['Studio']
    if data is None:
        await ctx.send("Cant find the Studio you are looking for")
        return
    em = Embed(title=data['name'])
    em.set_author(name='#'+str(data['id']))

    f_list = []
    m_list = []
    for i in sorted(data['media']['nodes'], key=lambda x: x['favourites'], reverse=True):
        title = i['title']
        fmt = i['format']
        if fmt == "MOVIE":
            m_list.append(title['english'] or title['romaji'] or title['native'])
        else:
            f_list.append(title['english'] or title['romaji'] or title['native'])
    f_list = '\n'.join(f_list[:10])
    m_list = '\n'.join(m_list[:10])
    if len(f_list) > 0:
        em.add_field(name="Animes: ", value=f_list, inline=False)
    if len(m_list) > 0:
        em.add_field(name="Movies:", value=m_list, inline=False)
    print(res)
    await ctx.send(embed=em)

bot.run(DISCORD_API_TOKEN)
