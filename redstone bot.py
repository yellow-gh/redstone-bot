import discord
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient
from discord import Member, Guild, User
import youtube_dl
import asyncio
import random
import time

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


antworten = ['Ja', 'Nein', 'Vielleicht', 'Wahrscheinlich', 'Sieht so aus', 'Sehr wahrscheinlich','Sehr unwahrscheinlich']
queue = []

bot = commands.Bot(command_prefix='PREFIX', intents=discord.Intents.all())
bot.remove_command('help')

@bot.event
async def on_ready():
    change_status.start()
    print('Wir sind eingeloggt als User {}'.format(bot.user.name))

@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game('ich spiele nicht ich arbeite'), status=discord.Status.online)
    await asyncio.sleep(5)
    await bot.change_presence(activity=discord.Game('[r!help]'), status=discord.Status.online)

@bot.command()
async def help(ctx):
    if ctx.author.bot == False:
        embed = discord.Embed(title='Hilfe für den redstone bot', description='Dies ist die hilfe zum redstone bot. Prefix: r!',color=0x22a7f0)
        embed.set_footer(text=f'angefordert von {ctx.author}')
        embed.add_field(name='join - Lässt den Bot dem Sprachkanal joinen',value='** **',inline=True)
        embed.add_field(name='queue - Fügt Musik der Wiedergabeliste hinzu',value='** **',inline=True)
        embed.add_field(name='remove - Entfernt Musik von der Wiedergabeliste',value='** **',inline=True)
        embed.add_field(name='play - Spielt Musik ab',value='** **',inline=True)
        embed.add_field(name='pause - Pausiert das abspielen von Musik',value='** **',inline=True)
        embed.add_field(name='resume - Setzt das abspielen von Musik fort',value='** **',inline=True)
        embed.add_field(name='view - Zeigt die Wiedergabeliste',value='** **',inline=True)
        embed.add_field(name='leave - Lässt den Bot den Sprachkanal verlassen',value='** **',inline=True)
        embed.add_field(name='stop - Stoppt das abspielen von Musik',value='** **',inline=True)
        embed.add_field(name='clear - Löscht Nachrichten (**nur für berechtigte**)',value='** **',inline=True)
        embed.add_field(name='ball - Wahrsagefunktion',value='** **',inline=True)
        embed.add_field(name='temp - Zeigt die Temperatur des servers vom bot an',value='** **',inline=True)
        embed.add_field(name='ping - zur überprüfung der Latenz',value='** **',inline=True)
        await ctx.send(embed=embed)


@bot.command()
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("Du bist mit keinem Sprachkanal verbunden")
        return

    else:
        channel = ctx.message.author.voice.channel

    await channel.connect()

@bot.command(name='queue')
async def queue_(ctx, url):
    global queue

    queue.append(url)
    await ctx.send(f'`{url}` zur Wiedergabeliste hinzugefügt')

@bot.command()
async def remove(ctx, number):
    global queue

    try:
        del(queue[int(number)])
        await ctx.send(f'Deine Wiedergabeliste ist jetzt `{queue}!`')

    except:
        await ctx.send('Deine Wiedergabeliste ist **Leer** oder das Lied ist nicht **enthalten**')

@bot.command()
async def play(ctx):
        global queue

        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            player = await YTDLSource.from_url(queue[0], loop=bot.loop)
            voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('**Spielt jetzt:** {}'.format(player.title))
        del(queue[0])

@bot.command()
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.pause()

@bot.command()
async def resume(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.resume()

@bot.command()
async def view(ctx):
    await ctx.send(f'Deine Wiedergabeliste ist `{queue}!`')

@bot.command()
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()

@bot.command()
async def stop(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.stop()

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=1):
    count = amount + 1
    await ctx.channel.purge(limit=count)
    await ctx.send('{0} Nachrichten wurden gelöscht'.format(amount), delete_after=5.0)

@bot.command()
async def ball(ctx, *, arg):
    await ctx.send('Ich versuche deine Frage `{0}` zu beantworten.'.format(arg), delete_after=2.0)
    await asyncio.sleep(2)
    await ctx.send('Ich kontaktiere das Orakel...', delete_after=2.0)
    await asyncio.sleep(2)
    await ctx.send('Deine Antwort zur Frage `{0}` lautet: `{1}`'.format(arg, random.choice(antworten)))

@ball.error
async def ball_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('keine Frage angegeben')

@bot.command()
async def temp(ctx):
    tempData = "/sys/class/thermal/thermal_zone0/temp"
    dateilesen = open(tempData, "r")
    temperatur = dateilesen.readline(2)
    dateilesen.close()
    await ctx.send('Die CPU hat ' + temperatur + ' Grad')

@bot.command()
async def ping(ctx):
    await ctx.send(f'**Pong!** Latenz: {round(bot.latency * 1000)}ms')

@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == CHANNELID:
        guild = bot.get_guild(SERVERID)
        role = guild.get_role(ROLEID)
        await payload.member.add_roles(role)

async def on_member_join(member):
    await member.send("WELCOMEMESSAGE")

bot.run('TOKEN')
