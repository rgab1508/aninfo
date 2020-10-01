import os
from discord.ext import commands

DISCORD_API_TOKEN = os.getenv('ANINFO_DIS_API_TOKEN')
COMMAND_PREFIX = os.getenv('ANINFO_COMMAND_PREFIX') or ","
bot = commands.Bot(command_prefix=COMMAND_PREFIX)

@bot.command()
async def info(ctx):
    print(ctx, dir(ctx), ctx.message.author)
    await ctx.send(f'hi {ctx.message.author}')


bot.run(DISCORD_API_TOKEN)
