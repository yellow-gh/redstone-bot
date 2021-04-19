import discord
from discord.ext import commands, tasks
import asyncio
import random

antworten = ['Ja', 'Nein', 'Vielleicht', 'Wahrscheinlich', 'Sieht so aus', 'Sehr wahrscheinlich', 'Sehr unwahrscheinlich']
teilnehmer = []
embedcollor = [0xdfff00, 0xfa00f0]
coinflip = ['kopf', 'zahl']

bot = commands.Bot(command_prefix='r!', intents=discord.Intents.all())
bot.remove_command('help')

@bot.event
async def on_ready():
    change_status.start()
    print('Bot wurde gestartet')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title='**Error** ',color=random.choice(embedcollor))
        embed.add_field(name='Befehl nicht gefunden',value='** **',inline=True)
        await ctx.send(embed=embed)

@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == 789478285205569559:
        guild = bot.get_guild(597787927476699157)
        mem = discord.utils.find(lambda m : m.id == 708230773219786793, guild.members)
        if not payload.member == mem:
            global teilnehmer
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            teilnehmer.append(member)

@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game('ich spiele nicht ich arbeite'), status=discord.Status.online)
    await asyncio.sleep(5)
    await bot.change_presence(activity=discord.Game('[r!help]'), status=discord.Status.online)

@bot.command()
async def help(ctx):
    if not ctx.author.bot:
        embed = discord.Embed(title='Hilfe für den redstone bot', description='Dies ist die hilfe zum redstone bot.(Eckige Klammern weglassen)',color=random.choice(embedcollor))
        embed.set_footer(text=f'angefordert von {ctx.author}')
        embed.add_field(name='**gstart** [text]',value='Startet ein Gewinnspiel (nur für Berechtigte)',inline=True)
        embed.add_field(name='**gchose**',value='wertet einen Gewinner aus (nur für Berechtigte)',inline=True)
        embed.add_field(name='**userinfo** [user]',value='Zeigt Informationen über User an',inline=True)
        embed.add_field(name='**8ball** [frage]',value='Wahrsagefunktion',inline=True)
        embed.add_field(name='**ping**',value='zur überprüfung der Latenz',inline=True)
        embed.add_field(name='**embed** [text]',value='sendet ein embed (nur für Berechtigte)',inline=True)
        embed.add_field(name='**flip**',value='coinflip funktion',inline=True)
        embed.add_field(name='**vid**',value='für video anoucementss',inline=True)
        await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def vid(ctx, link):
    await ctx.channel.purge(limit=1)
    guild = bot.get_guild(597787927476699157)
    ping = guild.get_role(792113253421154314)
    await ctx.send('{0} Neues Video {1}'.format(ping.mention ,link))

@vid.error
async def vid_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title='**Error** ',color=random.choice(embedcollor))
        embed.add_field(name='Du darft diesen Befehl nicht benutzen',value='** **',inline=True)
        await ctx.send(embed=embed)

    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='**Error** ',color=random.choice(embedcollor))
        embed.add_field(name='hmm da fehlt was',value='** **',inline=True)
        await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(change_nickname=True)
async def embed(ctx, *, text):
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title='👥 | {}'.format(ctx.author.name),color=random.choice(embedcollor))
    embed.add_field(name='{}'.format(text),value='** **',inline=True)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def gstart(ctx, *, arg):
    teilnehmer.clear()
    guild = bot.get_guild(597787927476699157)
    ping = guild.get_role(789530915268853811)
    embed = discord.Embed(title='**Gewinnspiel**',color=random.choice(embedcollor))
    embed.add_field(name='{}'.format(arg),value='** **',inline=True)
    embed.set_footer(text='Hostet by {}'.format(ctx.author))
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
async def gchose(ctx):
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

@gchose.error
async def gchose_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
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
async def ping(ctx):
    embed = discord.Embed(title='**Pong!**', description=f'Latenz: {round(bot.latency * 1000)}ms',color=random.choice(embedcollor))
    embed.set_footer(text=f'angefordert von {ctx.author}')
    await ctx.send(embed=embed)

@bot.command()
async def flip(ctx):
    embed = discord.Embed(title='**Coinflip**', description='{}'.format(random.choice(coinflip)),color=random.choice(embedcollor))
    embed.set_footer(text=f'angefordert von {ctx.author}')
    await ctx.send(embed=embed)
