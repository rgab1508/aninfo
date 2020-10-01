from discord.ext import commands

bot = commands.Bot(command_prefix='$')

@bot.command()
async def info(ctx):
    print(ctx, dir(ctx))


bot.run('NzYxMjEwMDkxMDU5NTQ0MDc1.X3XSJA.KohzUaFXQC2a6xn2mdavDgimu2Q')
