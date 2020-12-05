import discord
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient
import youtube_dl
import asyncio
import random
import time

antworten = ['Ja', 'Nein', 'Vielleicht', 'Wahrscheinlich', 'Sieht so aus', 'Sehr wahrscheinlich',
             'Sehr unwahrscheinlich']

autoroles = {
    ServerID: {'memberroles':[RoleID]}}

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
    'source_address': '0.0.0.0'
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


bot = commands.Bot(command_prefix='Prefix', intents=discord.Intents.all())

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

@bot.command(name='play', help='Spielt Musik ab')
async def play(ctx, url):
    if not ctx.author.voice:
        ctx.send('Du bist mit keinem Sprachkanal verbunden')
        return

    else:
        channel = ctx.message.author.voice.channel

    await channel.connect()

    server = ctx.message.guild
    voice_channel = server.voice_client

    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=bot.loop)
        voice_channel.play(player, after=lambda e: print('Player error: %s' %e) if e else None)

    await ctx.send(f'**Spielt jetzt:** {player.title}')

@play.error
async def play_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('kein Musikstück angegeben')

@bot.command(name='stop', help='Stoppt das abspielen von Musik')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()


@bot.command(name='clear', help='Löscht nachrichten')
@commands.has_permissions(manage_messages=True)
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
    await ctx.send('Deine Antwort zur Frage `{0}` lautet: `{1}`'.format(arg, random.choice(antworten)))

@ball.error
async def ball_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('keine Frage angegeben')

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

@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    channel = guild.get_channel(payload.channel_id)
    autoguild = autoroles.get(guild.id)
    if channel.id == ChannelID:
        if autoguild and autoguild['memberroles']:
            for roleId in autoguild['memberroles']:
                role = guild.get_role(roleId)
                if role:
                    await member.add_roles(role, reason='AutoRoles', atomic=True)

bot.run('Token')
