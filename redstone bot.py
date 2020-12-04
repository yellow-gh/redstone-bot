import discord
from discord.ext import commands, tasks
from discord import Member, Guild, User
from discord.utils import get
import asyncio
import random
import time

antworten = ['Ja', 'Nein', 'Vielleicht', 'Wahrscheinlich', 'Sieht so aus', 'Sehr wahrscheinlich',
             'Sehr unwahrscheinlich']

bot = commands.Bot(command_prefix='r!')

@bot.event
async def on_ready():
    change_status.start()
    print('Wir sind eingeloggt als User {}'.format(bot.user.name))

@tasks.loop(seconds=15)
async def change_status():
    await bot.change_presence(activity=discord.Game('ich spiele nicht ich arbeite'), status=discord.Status.online)
    await asyncio.sleep(5)
    await bot.change_presence(activity=discord.Game('Gäähn..Z..z..z'), status=discord.Status.online)
    await asyncio.sleep(5)
    await bot.change_presence(activity=discord.Game('[r!help]'), status=discord.Status.online)

@bot.command(name='clear', help='Löscht nachrichten')
async def clear(ctx, amount=1):
    count = amount + 1
    await ctx.channel.purge(limit=count)
    await ctx.send('{0} Nachrichten wurden gelöscht'.format(amount), delete_after=5.0)

@bot.command(name='ball', help='Wahrsagefunktion')
async def ball(ctx, *, arg):
    await ctx.send('Ich versuche deine Frage `{0}` zu beantworten.'.format(arg), delete_after=2.0)
    await asyncio.sleep(2)
    await ctx.send('Ich kontaktiere das Orakel...', delete_after=2.0)
    await asyncio.sleep(2)
    await ctx.send('Deine Antwort zur Frage `{0}` lautet: `{1}`'.format(arg,random.choice(antworten)))

@bot.command(name='temp', help='Zeigt die Temperatur des Servers vom Bot an')
async def temp(ctx):
    tempData = "/sys/class/thermal/thermal_zone0/temp"
    dateilesen = open(tempData, "r")
    temperatur = dateilesen.readline(2)
    dateilesen.close()
    await ctx.send('Die CPU hat ' + temperatur + ' Grad')

@bot.command(name='ping', help='zur überprüfung der Latenz')
async def ping(ctx):
    await ctx.send(f'**Pong!** Latenz: {round(bot.latency * 1000)}ms')

bot.run('token')
