import discord
from discord.ext import commands, tasks
from discord import Guild
from discord.voice_client import VoiceClient
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


antworten = ['Ja', 'Nein', 'Vielleicht', 'Wahrscheinlich', 'Sieht so aus', 'Sehr wahrscheinlich', 'Sehr unwahrscheinlich']
teilnehmer = []
embedcollor = [0xdfff00, 0xfa00f0]

bot = commands.Bot(command_prefix='r!', intents=discord.Intents.all())
bot.remove_command('help')

@bot.event
async def on_ready():
    change_status.start()
    print('Bot wurde gestartet')

@bot.event
async def on_member_join(member):
    if not member.bot:
        guild = bot.get_guild(597787927476699157)
        role = guild.get_role(722031383362404382)
        role2 = guild.get_role(789520194552332308)
        await member.add_roles(role)
        await member.add_roles(role2)
        embed = discord.Embed(title="Willkommen auf yellow_redstone's discord {} ".format(member.name),description='von redstone bot', color=random.choice(embedcollor))
        embed.add_field(name="Hallo auch von meiner seite, ich Organisiere den ganzen Kram am server. Aber nun viel spaß auf yellow_redstone's discord",value='** **',inline=True)
        try:
            if not member.dm_channel:
                await member.create_dm()
            await member.dm_channel.send(embed=embed)
        except discord.errors.Forbidden:
            print('Es konnte keine Willkommensnachricht an {} gesendet werden.'.format(member.name))

@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == 789531336187707422:
        if payload.emoji.name == "📢":
            guild = bot.get_guild(597787927476699157)
            role = guild.get_role(789542743726620712)
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            await member.add_roles(role)

    if payload.channel_id == 789531336187707422:
        if payload.emoji.name == "🎉":
            guild = bot.get_guild(597787927476699157)
            role = guild.get_role(789530915268853811)
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            await member.add_roles(role)

    if payload.channel_id == 789531336187707422:
        if payload.emoji.name == "❓":
            guild = bot.get_guild(597787927476699157)
            role = guild.get_role(790639841184055316)
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            await member.add_roles(role)

    if payload.channel_id == 789531336187707422:
        if payload.emoji.name == "🟥":
            guild = bot.get_guild(597787927476699157)
            role = guild.get_role(792113253421154314)
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            await member.add_roles(role)

    if payload.channel_id == 789478285205569559:
        guild = bot.get_guild(597787927476699157)
        mem = discord.utils.find(lambda m : m.id == 708230773219786793, guild.members)
        if not payload.member == mem:
            global teilnehmer
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            teilnehmer.append(member)

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.channel_id == 789531336187707422:
        if payload.emoji.name == "📢":
            guild = bot.get_guild(597787927476699157)
            role = guild.get_role(789542743726620712)
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            await member.remove_roles(role)

    if payload.channel_id == 789531336187707422:
        if payload.emoji.name == "🎉":
            guild = bot.get_guild(597787927476699157)
            role = guild.get_role(789530915268853811)
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            await member.remove_roles(role)

    if payload.channel_id == 789531336187707422:
        if payload.emoji.name == "❓":
            guild = bot.get_guild(597787927476699157)
            role = guild.get_role(790639841184055316)
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            await member.remove_roles(role)

    if payload.channel_id == 789531336187707422:
        if payload.emoji.name == "🟥":
            guild = bot.get_guild(597787927476699157)
            role = guild.get_role(792113253421154314)
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            await member.remove_roles(role)

@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game('ich spiele nicht ich arbeite'), status=discord.Status.online)
    await asyncio.sleep(5)
    await bot.change_presence(activity=discord.Game('[r!help]'), status=discord.Status.online)
    guild = bot.get_guild(597787927476699157)
    channel = guild.get_channel(791016242268864552)
    await channel.edit(name='«👥»Membercount : {}'.format(guild.member_count))

@bot.command()
async def help(ctx):
    if not ctx.author.bot:
        if ctx.author.guild_permissions.administrator:
            embed = discord.Embed(title='Hilfe für den redstone bot', description='Dies ist die hilfe zum redstone bot.(Eckige Klammern weglassen)',color=random.choice(embedcollor))
            embed.set_footer(text=f'angefordert von {ctx.author}')
            embed.add_field(name='**gstart** - [text] Startet ein Gewinnspiel (nur für Berechtigte)',value='** **',inline=True)
            embed.add_field(name='**gchose** - wertet einen Gewinner aus (nur für Berechtigte)',value='** **',inline=True)
            embed.add_field(name='**play** - [lied] Spielt Musik ab (nur für Berechtigte)',value='** **',inline=True)
            embed.add_field(name='**stop** - Stoppt das abspielen von Musik (nur für Berechtigte)',value='** **',inline=True)
            embed.add_field(name='**pause** - Pausiert das abspielen von Musik (nur für Berechtigte)',value='** **',inline=True)
            embed.add_field(name='**resume** - Setzt das abspielen von Musik fort (nur für Berechtigte)',value='** **',inline=True)
            embed.add_field(name='**userinfo** - [user] Zeigt Informationen über User an',value='** **',inline=True)
            embed.add_field(name='**clear** - [anzahl] Löscht Nachrichten (nur für Berechtigte)',value='** **',inline=True)
            embed.add_field(name='**8ball** - [frage] Wahrsagefunktion',value='** **',inline=True)
            embed.add_field(name='**temp** - Zeigt die Temperatur des servers vom bot an',value='** **',inline=True)
            embed.add_field(name='**ping** - zur überprüfung der Latenz',value='** **',inline=True)
            embed.add_field(name='**embed** - [text] sendet ein embed (nur für Berechtigte)',value='** **',inline=True)
            await ctx.send(embed=embed)

        elif ctx.author.guild_permissions.change_nickname and ctx.author.guild_permissions.view_audit_log:
            embed = discord.Embed(title='Hilfe für den redstone bot', description='Dies ist die hilfe zum redstone bot.(Eckige Klammern weglassen)',color=random.choice(embedcollor))
            embed.set_footer(text=f'angefordert von {ctx.author}')
            embed.add_field(name='**userinfo** - [user] Zeigt Informationen über User an',value='** **',inline=True)
            embed.add_field(name='**play** - [lied] Spielt Musik ab (nur für Berechtigte)',value='** **',inline=True)
            embed.add_field(name='**stop** - Stoppt das abspielen von Musik (nur für Berechtigte)',value='** **',inline=True)
            embed.add_field(name='**pause** - Pausiert das abspielen von Musik (nur für Berechtigte)',value='** **',inline=True)
            embed.add_field(name='**resume** - Setzt das abspielen von Musik fort (nur für Berechtigte)',value='** **',inline=True)
            embed.add_field(name='**clear** - [anzahl] Löscht Nachrichten (nur für Berechtigte)',value='** **',inline=True)
            embed.add_field(name='**8ball** - [frage] Wahrsagefunktion',value='** **',inline=True)
            embed.add_field(name='**temp** - Zeigt die Temperatur des servers vom bot an',value='** **',inline=True)
            embed.add_field(name='**ping** - zur überprüfung der Latenz',value='** **',inline=True)
            embed.add_field(name='**embed** - [text] sendet ein embed (nur für Berechtigte)',value='** **',inline=True)
            await ctx.send(embed=embed)

        elif ctx.author.guild_permissions.change_nickname:
            embed = discord.Embed(title='Hilfe für den redstone bot', description='Dies ist die hilfe zum redstone bot.(Eckige Klammern weglassen)',color=random.choice(embedcollor))
            embed.set_footer(text=f'angefordert von {ctx.author}')
            embed.add_field(name='**userinfo** - [user] Zeigt Informationen über User an',value='** **',inline=True)
            embed.add_field(name='**clear** - [anzahl] Löscht Nachrichten (nur für Berechtigte)',value='** **',inline=True)
            embed.add_field(name='**8ball** - [frage] Wahrsagefunktion',value='** **',inline=True)
            embed.add_field(name='**temp** - Zeigt die Temperatur des servers vom bot an',value='** **',inline=True)
            embed.add_field(name='**ping** - zur überprüfung der Latenz',value='** **',inline=True)
            embed.add_field(name='**embed** - [text] sendet ein embed (nur für Berechtigte)',value='** **',inline=True)
            await ctx.send(embed=embed)

        elif ctx.author.guild_permissions.view_audit_log:
            embed = discord.Embed(title='Hilfe für den redstone bot', description='Dies ist die hilfe zum redstone bot.(Eckige Klammern weglassen)',color=random.choice(embedcollor))
            embed.set_footer(text=f'angefordert von {ctx.author}')
            embed.add_field(name='**play** - [lied] Spielt Musik ab (nur für Berechtigte)',value='** **',inline=True)
            embed.add_field(name='**stop** - Stoppt das abspielen von Musik (nur für Berechtigte)',value='** **',inline=True)
            embed.add_field(name='**pause** - Pausiert das abspielen von Musik (nur für Berechtigte)',value='** **',inline=True)
            embed.add_field(name='**resume** - Setzt das abspielen von Musik fort (nur für Berechtigte)',value='** **',inline=True)
            embed.add_field(name='**userinfo** - [user] Zeigt Informationen über User an',value='** **',inline=True)
            embed.add_field(name='**clear** - [anzahl] Löscht Nachrichten (nur für Berechtigte)',value='** **',inline=True)
            embed.add_field(name='**8ball** - [frage] Wahrsagefunktion',value='** **',inline=True)
            embed.add_field(name='**temp** - Zeigt die Temperatur des servers vom bot an',value='** **',inline=True)
            embed.add_field(name='**ping** - zur überprüfung der Latenz',value='** **',inline=True)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title='Hilfe für den redstone bot', description='Dies ist die hilfe zum redstone bot.(Eckige Klammern weglassen)',color=random.choice(embedcollor))
            embed.set_footer(text=f'angefordert von {ctx.author}')
            embed.add_field(name='**userinfo** - [user] Zeigt Informationen über User an',value='** **',inline=True)
            embed.add_field(name='**clear** - [anzahl] Löscht Nachrichten (nur für Berechtigte)',value='** **',inline=True)
            embed.add_field(name='**8ball** - [frage] Wahrsagefunktion',value='** **',inline=True)
            embed.add_field(name='**temp** - Zeigt die Temperatur des servers vom bot an',value='** **',inline=True)
            embed.add_field(name='**ping** - zur überprüfung der Latenz',value='** **',inline=True)
            await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(change_nickname=True)
async def embed(ctx, *, text):
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title='👥 | {}'.format(ctx.author.name),color=random.choice(embedcollor))
    embed.add_field(name='{}'.format(text),value='** **',inline=True)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@embed.error
async def embed_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title='**Error** ',color=random.choice(embedcollor))
        embed.add_field(name='Du darft diesen Befehl nicht benutzen',value='** **',inline=True)
        await ctx.send(embed=embed)

    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='**Error** ',color=random.choice(embedcollor))
        embed.add_field(name='hmm da fehlt was',value='** **',inline=True)
        await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def gstart(ctx, *, arg):
    teilnehmer.clear()
    guild = bot.get_guild(597787927476699157)
    ping = guild.get_role(789530915268853811)
    embed = discord.Embed(title='**Gewinnspiel**',color=random.choice(embedcollor))
    embed.add_field(name='{}'.format(arg),value='** **',inline=True)
    embed.set_footer(text=f'Hostet by {ctx.author}')
    await ctx.channel.purge()
    await ctx.send('{}'.format(ping.mention))
    mess = await ctx.send(embed=embed)
    await mess.add_reaction('🎉')

@gstart.error
async def gstart_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title='**Error** ',color=random.choice(embedcollor))
        embed.add_field(name='Du darft diesen Befehl nicht benutzen',value='** **',inline=True)
        await ctx.send(embed=embed)

    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='**Error** ',color=random.choice(embedcollor))
        embed.add_field(name='hmm da fehlt was',value='** **',inline=True)
        await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def chose(ctx):
    winner = random.choice(teilnehmer)
    embed = discord.Embed(title='**Gewinnspiel**',color=random.choice(embedcollor))
    embed.add_field(name='🥇{} hat gewonnen'.format(winner),value='** **',inline=True)
    await ctx.send('{}'.format(winner.mention))
    await ctx.send(embed=embed)
    embed = discord.Embed(title='**Gewinnspiel**',color=random.choice(embedcollor))
    embed.add_field(name="du hast bei einem Gewinnspiel gewonnen" ,value='** **',inline=True)
    try:
        if not winner.dm_channel:
            await winner.create_dm()
        await winner.dm_channel.send(embed=embed)
    except discord.errors.Forbidden:
        print('Der hat wohl keinen bock zu gewinnen')

@chose.error
async def chose_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title='**Error** ',color=random.choice(embedcollor))
        embed.add_field(name='Du darft diesen Befehl nicht benutzen',value='** **',inline=True)
        await ctx.send(embed=embed)

@bot.command()
@commands.has_role(784843450025508905)
async def play(ctx, *, url):
    guild = bot.get_guild(597787927476699157)
    member = discord.utils.find(lambda m : m.id == 708230773219786793, guild.members)
    if not member.voice:
        if not ctx.message.author.voice:
            embed = discord.Embed(title='**Error** ',color=random.choice(embedcollor))
            embed.add_field(name='Du bist mit keinem Sprachkanal verbunden',value='** **',inline=True)
            await ctx.send(embed=embed)
            return

        else:
            channel = ctx.message.author.voice.channel

        await channel.connect()

    server = ctx.message.guild
    voice_channel = server.voice_client
    if not voice_channel.is_playing():
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        embed = discord.Embed(title='**Spielt jetzt:** ', description='**{}**'.format(player.title),color=random.choice(embedcollor))
        embed.set_footer(text=f'hinzugefügt von {ctx.author}')
        await ctx.send(embed=embed)

    else:
        embed = discord.Embed(title='**Error** ',color=random.choice(embedcollor))
        embed.add_field(name='du kannst aktuel keine Musik abspielen', value='** **', inline=True)
        await ctx.send(embed=embed)

@play.error
async def play_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        embed = discord.Embed(title='**Error** ',color=random.choice(embedcollor))
        embed.add_field(name='Du darft diesen Befehl nicht benutzen', value='** **', inline=True)
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='**Error** ',color=random.choice(embedcollor))
        embed.add_field(name='Du hast kein Musikstück angegeben', value='** **', inline=True)
        await ctx.send(embed=embed)

@bot.command()
@commands.has_role(784843450025508905)
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.pause()

@pause.error
async def pause_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        embed = discord.Embed(title='**Error** ',color=random.choice(embedcollor))
        embed.add_field(name='Du darft diesen Befehl nicht benutzen',value='** **',inline=True)
        await ctx.send(embed=embed)

@bot.command()
@commands.has_role(784843450025508905)
async def resume(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.resume()

@resume.error
async def resume_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        embed = discord.Embed(title='**Error** ',color=random.choice(embedcollor))
        embed.add_field(name='Du darft diesen Befehl nicht benutzen',value='** **',inline=True)
        await ctx.send(embed=embed)

@bot.command(name='stop')
@commands.has_role(784843450025508905)
async def stop_(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_client = ctx.message.guild.voice_client
    voice_channel.stop()
    await voice_client.disconnect()

@stop_.error
async def stop_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        embed = discord.Embed(title='**Error** ',color=random.choice(embedcollor))
        embed.add_field(name='Du darft diesen Befehl nicht benutzen',value='** **',inline=True)
        await ctx.send(embed=embed)

@bot.command()
async def userinfo(ctx, member : discord.Member):
    try:
        embed = discord.Embed(title='Userinfo für {}'.format(member.name),description='Dies ist eine Userinfo für den User {}'.format(member.mention),color=random.choice(embedcollor))
        embed.add_field(name='Server beigetreten', value=member.joined_at.strftime('%d/%m/%Y, %H:%M:%S'),inline=True)
        embed.add_field(name='Discord beigetreten', value=member.created_at.strftime('%d/%m/%Y, %H:%M:%S'),inline=True)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f'angefordert von {ctx.author}')
    except:
        print('userinfo error')
    await ctx.send(embed=embed)

@userinfo.error
async def userinfo_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='**Error** ',color=random.choice(embedcollor))
        embed.add_field(name='Du hast keinen User angegeben',value='** **',inline=True)
        await ctx.send(embed=embed)

    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(title='**Error** ',color=random.choice(embedcollor))
        embed.add_field(name='User wurde nicht gefunden',value='** **',inline=True)
        await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=1):
    count = amount + 1
    await ctx.channel.purge(limit=count)
    embed = discord.Embed(title='**Clear**', description='{0} Nachrichten wurden gelöscht'.format(amount),color=random.choice(embedcollor))
    embed.set_footer(text=f'angefordert von {ctx.author}')
    await ctx.send(embed=embed, delete_after=5.0)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title='**Error** ',color=random.choice(embedcollor))
        embed.add_field(name='Du darft diesen Befehl nicht benutzen',value='** **',inline=True)
        await ctx.send(embed=embed)

@bot.command(name='8ball')
async def ball(ctx, *, arg):
    embed = discord.Embed(title='**8ball**', description='Ich versuche deine Frage `{0}` zu beantworten.'.format(arg),color=random.choice(embedcollor))
    embed.set_footer(text=f'angefordert von {ctx.author}')
    await ctx.send(embed=embed, delete_after=2.0)
    await asyncio.sleep(2)
    embed = discord.Embed(title='**8ball**', description='Ich kontaktiere das Orakel...',color=random.choice(embedcollor))
    embed.set_footer(text=f'angefordert von {ctx.author}')
    await ctx.send(embed=embed, delete_after=2.0)
    await asyncio.sleep(2)
    embed = discord.Embed(title='**8ball**', description='Deine Antwort zur Frage `{0}` lautet: `{1}`'.format(arg, random.choice(antworten)),color=random.choice(embedcollor))
    embed.set_footer(text=f'angefordert von {ctx.author}')
    await ctx.send(embed=embed)

@ball.error
async def ball_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='**Error** ', description='',color=random.choice(embedcollor))
        embed.add_field(name='Du hast keine Frage angegeben',value='** **',inline=True)
        await ctx.send(embed=embed)

@bot.command()
async def temp(ctx):
    tempData = "/sys/class/thermal/thermal_zone0/temp"
    dateilesen = open(tempData, "r")
    temperatur = dateilesen.readline(2)
    dateilesen.close()
    embed = discord.Embed(title='Temperatur', description='Die CPU hat ' + temperatur + ' Grad',color=random.choice(embedcollor))
    embed.set_footer(text=f'angefordert von {ctx.author}')
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    embed = discord.Embed(title='**Pong!**', description=f'Latenz: {round(bot.latency * 1000)}ms',color=random.choice(embedcollor))
    embed.set_footer(text=f'angefordert von {ctx.author}')
    await ctx.send(embed=embed)

bot.run('')
