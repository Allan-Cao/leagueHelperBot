'''
TODO
- DISCORD JOIN LINK https://discord.com/api/oauth2/authorize?client_id=714568795456274472&permissions=3213376&scope=bot
- Apply for Personal API Key
'''
# Custom op.gg scraper
import op_gg_scraper
import requests as r
from bs4 import BeautifulSoup
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
import discord
from riotwatcher import LolWatcher, ApiError
from tinydb import TinyDB, Query
from gtts import gTTS
import champion_gg_scraper
import sys
from PIL import Image
import re
import random
import glob

music = glob.glob("music/*.mp3")
cdn = 'https://ddragon.leagueoflegends.com/cdn/img/'
regex = re.compile('[^a-zA-Z]')
API_KEY = "RGAPI-22e57aa2-4d5e-4195-a11f-b6296653c3b9"
DISCORD_TOKEN = "NzE0NTY4Nzk1NDU2Mjc0NDcy.XswkMA.tG2gh0cgQevOPLLPY22OGts4i5U"
LOL = LolWatcher(API_KEY)
REGION = "na1"
db = TinyDB('db.json')
ffmpeg_options = {'options': '-filter:a "volume=0.25"'}
tilt_masters = [229696743774748673, 203622383683108864, 265035781733613568]
runesReforged = r.get('http://ddragon.leagueoflegends.com/cdn/10.11.1/data/en_US/runesReforged.json').json()
complete_runes = {}
for rune in runesReforged:
    for sub_rune in rune['slots']:
        for sub_sub_rune in sub_rune['runes']:
            complete_runes[sub_sub_rune['key']] = sub_sub_rune['icon']
'''
primary_images = {'Domination':'perk-images/Styles/7200_Domination.png',
                 'Inspiration':'perk-images/Styles/7203_Whimsy.png',
                 'Precision':'perk-images/Styles/7201_Precision.png',
                 'Resolve':'perk-images/Styles/7204_Resolve.png',
                 'Sorcery':'perk-images/Styles/7202_Sorcery.png'}
'''
primary_images = {'Domination':'cache/7200_Domination.png',
                 'Inspiration':'cache/7203_Whimsy.png',
                 'Precision':'cache/7201_Precision.png',
                 'Resolve':'cache/7204_Resolve.png',
                 'Sorcery':'cache/7202_Sorcery.png'}
shard_images = [
    ['https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perk-images/statmods/statmodsadaptiveforceicon.png','https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perk-images/statmods/statmodsattackspeedicon.png','https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perk-images/statmods/statmodscdrscalingicon.png'],
    ['https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perk-images/statmods/statmodsadaptiveforceicon.png','https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perk-images/statmods/statmodsarmoricon.png','https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perk-images/statmods/statmodsmagicresicon.png'],
    ['https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perk-images/statmods/statmodshealthscalingicon.png','https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perk-images/statmods/statmodsarmoricon.png','https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perk-images/statmods/statmodsmagicresicon.png']]
def get_img(filename,which_rune,rune_type):
    if rune_type == 0:
        return
        '''
        url = primary_images[which_rune.title()]
        img_data = r.get(cdn + url).content
        with open(filename, 'wb') as handler:
            handler.write(img_data)
        '''
    elif rune_type == 1:
        secondary = regex.sub('', which_rune.title())
        url = complete_runes[secondary]
        img_data = r.get(cdn + url).content
        with open(filename, 'wb') as handler:
            handler.write(img_data)
    elif rune_type == 2:
        url = shard_images[which_rune[0]][which_rune[1]]
        img_data = r.get(url).content
        with open(filename, 'wb') as handler:
            handler.write(img_data)
def runes_to_image(runes,primary_images,complete_runes,shard_images):
    get_img('2.png',runes[0][1][0],1)
    get_img('3.png',runes[0][1][1],1)
    get_img('4.png',runes[0][1][2],1)
    get_img('5.png',runes[0][1][3],1)

    images = [Image.open(x).resize((64, 64)) for x in [primary_images[runes[0][0]], '2.png', '3.png', '4.png', '5.png']]
    widths, heights = zip(*(i.size for i in images))

    y_offset = 10
    total_height = sum(heights) + (y_offset*len(images)) + y_offset
    max_width = 84
    primary_runes = Image.new('RGB', (max_width, total_height), (255, 255, 255))
    for im in images:
      primary_runes.paste(im, (10,y_offset))
      y_offset += im.size[1] + 10
    get_img('2.png',runes[1][1][0],1)
    get_img('3.png',runes[1][1][1],1)
    images = [Image.open(x).resize((64, 64)) for x in [primary_images[runes[1][0]], '2.png', '3.png']]
    widths, heights = zip(*(i.size for i in images))
    y_offset = 10
    total_height = sum(heights) + (y_offset*len(images)) + y_offset
    max_width = 84
    secondary = Image.new('RGB', (max_width, total_height), (255, 255, 255))
    for im in images:
      secondary.paste(im, (10,y_offset))
      y_offset += im.size[1] + 10

    get_img('4.png',[0,runes[2][0]],2)
    get_img('5.png',[1,runes[2][1]],2)
    get_img('6.png',[2,runes[2][2]],2)
    images = [Image.open(x).resize((64, 64)) for x in ['4.png', '5.png','6.png']]
    widths, heights = zip(*(i.size for i in images))
    y_offset = 10
    total_height = sum(heights) + (y_offset*len(images)) + y_offset
    max_width = 84
    shards = Image.new('RGB', (max_width, total_height), (255, 255, 255))
    for im in images:
      shards.paste(im, (10,y_offset))
      y_offset += im.size[1] + 10
      
    images = [primary_runes,secondary,shards]
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)
    new_im = Image.new('RGB', (total_width, max_height), (255, 255, 255))
    x_offset = 0
    for im in images:
      new_im.paste(im, (x_offset,0))
      x_offset += im.size[0]
    new_im.save('rune.png')
    return

try:
    latest = LOL.data_dragon.versions_for_region(REGION)['n']['champion']
    CHAMPS = LOL.data_dragon.champions(latest, False, 'en_US')
    FREE_ROTATION = LOL.champion.rotations(REGION)
except ApiError as err:
    if err.response.status_code == 429:
        print("API Rate Limiting. Please try again later.")
    elif err.response.status_code == 404:
        print("Unknown API error")
    else:
        raise

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    game = discord.Game("League of Legends")
    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.event
async def on_message(message):
    if message.author == bot.user:
            return
    await bot.process_commands(message)

@bot.command(name='user',
            brief='Summoner names are used in the "ingame" command',
            pass_context=True)
async def user(ctx, *args):
    if len(args) == 1:
        if args[0].lower() == "query":
            summoners = db.search(Query().discord == ctx.author.id)
            await ctx.send([summoner['summoner'] for summoner in summoners])
    elif len(args) == 2:
        if args[0].lower() == "add":
            lower_summoner = args[1].lower()
            if len(db.search((Query().discord == ctx.author.id) & (Query().summoner == lower_summoner))) == 0:
                if len(db.search((Query().discord == ctx.author.id))) == 1:
                    await ctx.send("Multiple accounts are not supported yet.")
                else:
                    try:
                        response = LOL.summoner.by_name(REGION, args[1])
                        db.insert({'name':response['name'], 'summoner': response['name'].lower(),\
                                   'discord': ctx.author.id, 'id': response['id'],\
                                   'accountid' : response['accountId'], 'puuid': response['puuid']})
                        await ctx.send("The summoner {0} at level {1} has been added".format(db.search(Query().summoner == lower_summoner)[0]['name'],response['summonerLevel']))
                    except ApiError as err:
                        if err.response.status_code == 429:
                            await ctx.send("API Rate Limiting. Please try again later.")
                        elif err.response.status_code == 404:
                            await ctx.send('Summoner could not be found')
                        else:
                            raise

            else:
                await ctx.send("You have already added your summoner {0}".format(args[1]))
        elif args[0].lower() == "remove":
            lower_summoner = args[1].lower()
            summoners = db.search((Query().discord == ctx.author.id) & (Query().summoner == lower_summoner))
            if len(summoners) == 0:
                await ctx.send("I could not find your summoner")
            elif len(summoners) == 1:
                if summoners[0]['summoner'] == lower_summoner:
                    await ctx.send(f"The summoner {db.search(Query().summoner == lower_summoner)[0]['name']} has been removed")
                    db.remove((Query().discord == ctx.author.id) & (Query().summoner == lower_summoner))
                    
                else:
                    await ctx.send("An unknown error has occured. Allan you messed up!!!")
            else:
                await ctx.send("I am confused. Allan please help")
        else:
            await ctx.send("Available commands are add, remove and query")
    else:
        await ctx.send("Unknown summoner. Try $user add <summoner> or $user remove <summoner> or $user query")

@bot.command(name='debug',
            category='test debug',
            brief='Probably will contain some test commands',
            pass_context=True)
async def debug(ctx):
    #await ctx.send(" ".join(args))
    await ctx.send(db.search(Query().discord == ctx.author.id))

@bot.command(name='audiodebug',
            brief='Audio test command',
            pass_context=True)
async def audiodebug(ctx, *args):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice == None:
        await ctx.send("I'm currently not in a voice channel")
        return
    elif voice and voice.is_playing():
        voice.stop()
        gTTS(' '.join([word for word in args])).save('tts.mp3')
        voice.play(discord.FFmpegPCMAudio("tts.mp3",executable='ffmpeg'))
    else:
        gTTS(' '.join([word for word in args])).save('tts.mp3')
        voice.play(discord.FFmpegPCMAudio("tts.mp3",executable='ffmpeg'))
        
@bot.command(name='join',
            brief='Tries to join the current channel the message author is in',
            pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    if not channel or channel == None:
        await ctx.send("Join a voice channel before running this command", delete_after=20)
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await ctx.send("I'm already in a voice channel", delete_after=20)
    else:
        await ctx.send('Joining the call. Your channel is {0}'.format(channel), delete_after=20)
        voice = await channel.connect()

@bot.command(name='leave',
            brief='Tries to leave the current channel the message author is in',
            pass_context=True)
async def leave(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice == None:
        await ctx.send("I'm currently not in a voice channel", delete_after=20)
        return
    if voice and voice.is_connected():
        await ctx.send('Disconnecting', delete_after=20)
        await voice.disconnect()

@bot.command(name='tilted',
            brief='Tries to untilt you with the power of music',
            pass_context=True)
async def tilted(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice == None:
        await ctx.send("I'm currently not in a voice channel", delete_after=20)
        return
    else:
        voice.play(discord.FFmpegPCMAudio(random.choice(music),executable='ffmpeg', **ffmpeg_options))

@bot.command(name='marcoistilted',
            brief='Tries to untilt Marco',
            pass_context=True)
async def marcoistilted(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice == None:
        await ctx.send("I'm currently not in a voice channel", delete_after=20)
        return
    else:
        source = discord.FFmpegPCMAudio("marco.mp3",executable='ffmpeg', **ffmpeg_options)
        voice.play(source)

@bot.command(name='volume', aliases=['vol'], pass_context=True)
async def volume(ctx, *, vol: float):
    try:
        if vol > 0 and vol < 100:
            ffmpeg_options['options']= f'-filter:a "volume={vol/100}"'
            await ctx.send(f'**`{ctx.author}`**: Set the volume to **{vol}%**', delete_after=20)
    except:
        await ctx.send('Unknown error occured', delete_after=20)

@bot.command(name='marcoisverytilted',
            brief='Tries to untilt Marco with even more music',
            pass_context=True)
async def marcoisverytilted(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice == None:
        await ctx.send("I'm currently not in a voice channel", delete_after=20)
        return
    else:
        voice.play(discord.FFmpegPCMAudio("marco2.mp3",executable='ffmpeg', **ffmpeg_options))


@bot.command(name='pause',
            brief='Pauses the music',
            pass_context=True)
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice == None:
        await ctx.send("I'm currently not in a voice channel", delete_after=20)
        return
    if voice and voice.is_playing():
        if ctx.author.id in tilt_masters:
            await ctx.send("I'm sorry but I can't let you be tilted", delete_after=20)
        else:
            voice.pause()
    else:
        await ctx.send("I'm not playing any music right now", delete_after=20)
        return

@bot.command(name='resume',
            brief='Resumes the music',
            pass_context=True)
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice == None:
        await ctx.send("I'm currently not in a voice channel", delete_after=20)
        return
    if voice and voice.is_paused():
        voice.resume()
    else:
        await ctx.send("I don't think the music is paused.", delete_after=20)
        return

@bot.command(name='stop',
            brief='Stops the music',
            pass_context=True)
async def stop(ctx): 
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice == None:
        await ctx.send("I'm currently not in a voice channel", delete_after=20)
        return
    if voice and (voice.is_paused() or voice.is_playing()):
        if ctx.author.id in tilt_masters:
            await ctx.send("I'm sorry but I can't let you be tilted", delete_after=20)
        else:
            voice.stop()
    else:
        await ctx.send("I don't think the music is paused.", delete_after=20)
        return

@bot.command(name='runes',
            brief='Displays champion runes. runes [name] [lane]',
            pass_context=True)
async def runes(ctx, *args):
    try:
        if args[-1] == 'unmute':
            voice = get(bot.voice_clients, guild=ctx.guild)
            args = tuple(list(args[:-1]))
        else:
            args = tuple(list(args))
            voice = None
    except:
        await ctx.send("An error occured while getting runes (debug 1)")
    if len(args) == 2:
        try:
            nums = {0: 'Zero', 1: 'One', 2: 'Two'}
            _runes = op_gg_scraper.get_runes(args[1],args[0])
            rune_set = _runes[0]
            rune_tts = f"Primary Path is {rune_set[0][0]}, {rune_set[0][1][0]}, {rune_set[0][1][1]}, {rune_set[0][1][2]}, {rune_set[0][1][3]} \
                        Secondary Path is {rune_set[1][0]}, {rune_set[1][1][0]}, {rune_set[1][1][1]} \
                        Shards are {nums[rune_set[2][0]]}, {nums[rune_set[2][1]]}, {nums[rune_set[2][2]]}"
            await ctx.send(f"Primary Path is {rune_set[0][0]}, {rune_set[0][1][0]}, {rune_set[0][1][1]}, {rune_set[0][1][2]}, {rune_set[0][1][3]}\n\
Secondary Path is {rune_set[1][0]}, {rune_set[1][1][0]}, {rune_set[1][1][1]}\n\
Shards are {nums[rune_set[2][0]]}, {nums[rune_set[2][1]]}, {nums[rune_set[2][2]]}")
            runes_to_image(rune_set,primary_images,complete_runes,shard_images)
            with open('rune.png', 'rb') as f:
                picture = discord.File(f)
            await ctx.send(file=picture)
            if voice == None or (voice.is_paused() or voice.is_playing()):
                return
            else:
                gTTS(rune_tts).save('tts.mp3')
                voice.play(discord.FFmpegPCMAudio("tts.mp3",executable='ffmpeg'))
        except:
            await ctx.send("An error occured while getting runes (debug 2)")
    elif len(args) == 3:
        try:
            nums = {0: 'Zero', 1: 'One', 2: 'Two'}
            _runes = op_gg_scraper.get_runes(args[1],args[0])
            rune_set = _runes[0]
            paths = {'primary':f"Primary Path is {rune_set[0][0]}, {rune_set[0][1][0]}, {rune_set[0][1][1]}, {rune_set[0][1][2]}, {rune_set[0][1][3]}",
                     'secondary':f"Secondary Path is {rune_set[1][0]}, {rune_set[1][1][0]}, {rune_set[1][1][1]}",
                     'shards':f"Shards are {nums[rune_set[2][0]]}, {nums[rune_set[2][1]]}, {nums[rune_set[2][2]]}"}
            await ctx.send(paths[args[2]])
            if voice == None:
                return
            elif voice and (voice.is_paused() or voice.is_playing()):
                return
            else:
                gTTS(paths[args[2]]).save('tts.mp3')
                voice.play(discord.FFmpegPCMAudio("tts.mp3",executable='ffmpeg'))
        except:
            await ctx.send("An error occured while getting runes (debug 3)")                    
    else:
        await ctx.send("Unknown arguments. Try runes [name] [lane]")

@bot.command(name='build',
            brief='build [name] [lane] [starter/build/boots/none to show all]',
            pass_context=True)
async def build(ctx, *args):
    if args[-1] == 'unmute':
        voice = get(bot.voice_clients, guild=ctx.guild)
        args = tuple(list(args[:-1]))
    else:
        args = tuple(list(args))
        voice = None
    if len(args) == 3:
        try:
            _builds = dict(op_gg_scraper.get_build(args[1],args[0]))
            build_paths = {'starter':_builds['starter_items_1'],
                           'build':_builds['build_1'],
                           'boots':_builds['boots_1'],}
            await ctx.send(", ".join(build_paths[args[2]]))
            if voice == None:
                return
            elif voice and (voice.is_paused() or voice.is_playing()):
                await ctx.send("I'm talking right now. Use the command stop to stop it.")
            else:
                gTTS(f"{args[0]} {args[1]} {args[2]} items are"+" ".join(build_paths[args[2]])).save('tts.mp3')
                voice.play(discord.FFmpegPCMAudio("tts.mp3",executable='ffmpeg'))
        except:
            await ctx.send("An error occured while getting builds")
    elif len(args) == 2:
        try:
            _builds = dict(op_gg_scraper.get_build(args[1],args[0]))
            await ctx.send(f"{args[0]} {args[1]} starter items are "+", ".join(_builds['starter_items_1'])+'\n'+\
                           f"Complete build is "+", ".join(_builds['build_1'])+'\n'+\
                           f"Boots are "+", ".join(_builds['boots_1']))
            if voice == None:
                return
            elif voice and (voice.is_paused() or voice.is_playing()):
                await ctx.send("I'm talking right now. Use the command stop to stop it.")
            else:
                gTTS((f"{args[0]} {args[1]} starter items are "+", ".join(_builds['starter_items_1'])+\
                       f" Complete build is "+", ".join(_builds['build_1'])+\
                       f" Boots are "+", ".join(_builds['boots_1']))).save('tts.mp3')
                voice.play(discord.FFmpegPCMAudio("tts.mp3",executable='ffmpeg'))
        except:
            await ctx.send("An error occured while getting builds", delete_after=20)
    else:
        await ctx.send("Unknown arguments. Try build [name] [lane] [starter, build, boots]", delete_after=20)
                
@bot.command(name='skillorder',
            brief='Displays champion skill order. skillorder [name] [lane]',
            pass_context=True)
async def skillorder(ctx, *args):
    if args[-1] == 'unmute':
        voice = get(bot.voice_clients, guild=ctx.guild)
        args = tuple(list(args[:-1]))
    else:
        args = tuple(list(args))
        voice = None
    if len(args) == 2:
        try:
            _skillorder = op_gg_scraper.get_skill_order(args[1],args[0])
            await ctx.send(", ".join([(skill) for skill in _skillorder]))
            if voice == None:
                return
            elif voice and (voice.is_paused() or voice.is_playing()):
                return
            else:
                gTTS(f"The skill order for {args[0]} {args[1]} is "+", ".join([(skill) for skill in _skillorder])).save('tts.mp3')
                voice.play(discord.FFmpegPCMAudio("tts.mp3",executable='ffmpeg'))
        except:
            await ctx.send("An error occured while getting builds", delete_after=20)   
    else:
        await ctx.send("Unknown arguments. Try skillorder [name] [lane]", delete_after=20)
        
@bot.command(name='synergy',
            brief='synergy [adc] [support] [elo (bronze,silver,gold,plat,platplus)]',
            pass_context=True)
async def synergy(ctx, *args):
    if args[-1] == 'unmute':
        voice = get(bot.voice_clients, guild=ctx.guild)
        args = tuple(list(args[:-1]))
    else:
        args = tuple(list(args))
        voice = None
    if len(args) == 3:
        wr = champion_gg_scraper.get_synergy(args[0],args[1],args[2])
        if wr == None:
            await ctx.send("An error occured while getting synergy.")
            return
        if wr > 52:
            msg = f"{args[0]} and {args[1]} have strong synergy with a win rate of {wr} percent"
        elif wr > 50:
            msg = f"{args[0]} and {args[1]} have moderate synergy with a win rate of {wr} percent"
        else:
            msg = f"{args[0]} and {args[1]} have weak synergy with a win rate of {wr} percent"
        await ctx.send(msg)
        if voice == None:
            return
        elif voice and (voice.is_paused() or voice.is_playing()):
            return
        else:
            gTTS(msg).save('tts.mp3')
            voice.play(discord.FFmpegPCMAudio("tts.mp3",executable='ffmpeg'))
    elif len(args) == 2:
        wr = champion_gg_scraper.get_synergy(args[0],args[1])
        if wr == None:
            await ctx.send("An error occured while getting synergy.")
            return
        if wr > 51:
            msg = f"{args[0]} and {args[1]} have strong synergy with a win rate of {wr} percent"
        elif wr > 50:
            msg = f"{args[0]} and {args[1]} have moderate synergy with a win rate of {wr} percent"
        else:
            msg = f"{args[0]} and {args[1]} have weak synergy with a win rate of {wr} percent"
        await ctx.send(msg)
        if voice == None:
            return
        elif voice and (voice.is_paused() or voice.is_playing()):
            return
        else:
            gTTS(msg).save('tts.mp3')
            voice.play(discord.FFmpegPCMAudio("tts.mp3",executable='ffmpeg'))
    else:
        await ctx.send("Unknown arguments. Try synergy [adc] [support] [elo (bronze,silver,gold,plat,platplus)]")
        
@bot.command(name='about',
             brief='Displays information about the champion from the Riot API',
             pass_context = True)
async def about(ctx, *args):
    if args[-1] == 'unmute':
        voice = get(bot.voice_clients, guild=ctx.guild)
        args = tuple(list(args[:-1]))
    else:
        args = tuple(list(args))
        voice = None
    champion = ''.join(args)
    try:
        champ_data = CHAMPS['data'][champion]
        champ_type = ' and '.join(CHAMPS['data'][champion]['tags'])
        champ_name = champ_data['name']
        await ctx.send(f'{champ_name} is a {champ_type}')
        if voice == None:
            return
        elif voice and (voice.is_paused() or voice.is_playing()):
            return
        else:
            gTTS(f'{champ_name} is a {champ_type}').save('tts.mp3')
            voice.play(discord.FFmpegPCMAudio("tts.mp3",executable='ffmpeg'))
    except:
        await ctx.send("Unknown champion. Try about [champion]")
        
@bot.command(name='ingame', 
            brief='Displays helpful information about your current game',
            pass_context = True)
async def ingame(ctx, *args):
    try:
        
        more_game_data = LOL.spectator.by_summoner(REGION, db.search(Query().discord == ctx.author.id)[0]['id'])
        await ctx.send("Able to find your game. However, ingame data is currently in development")
        for participant in more_game_data['participants']:
            if participant['summonerId'] == db.search(Query().discord == 645940845245104130)[2]['id']:
                await ctx.send(f"Your team is {participant['teamId']} and your summoner is {participant['summonerName']}")
    except ApiError as err:
        if err.response.status_code == 429:
            await ctx.send("API Rate limiting error. Try again later.", delete_after=20)
        elif err.response.status_code == 404:
            await ctx.send("Try again later. I am able to get your game data once you are in the loading screen.", delete_after=20)
        else:
            await ctx.send("Very large error. Tell Allan to come fix me pls lol.", delete_after=20)
    '''voice = get(bot.voice_clients, guild=ctx.guild)
    champion = ''.join(args)
    try:
        champ_data = CHAMPS['data'][champion]
        champ_type = ' and '.join(CHAMPS['data'][champion]['tags'])
        champ_name = champ_data['name']
        await ctx.send(f'{champ_name} is a {champ_type}')
        if voice == None:
            return
        elif voice and (voice.is_paused() or voice.is_playing()):
            return
        else:
            gTTS(f'{champ_name} is a {champ_type}').save('tts.mp3')
            voice.play(discord.FFmpegPCMAudio("tts.mp3",executable='ffmpeg'))
    except:
        await ctx.send("Unknown champion. Try about [champion]")'''

@bot.command(name='ability', 
            brief='Displays champion abilities',
            pass_context = True)
async def ability(ctx, *args):
    await ctx.send("In Development", delete_after=20)
    '''
    if len(args) == 2:
        try:
            if args[0].lower() == 'passive':
                pass
        except:
            ctx.send('Error witht he command')
    voice = get(bot.voice_clients, guild=ctx.guild)
    champion = ''.join(args)
    try:
        champ_data = CHAMPS['data'][champion]
        champ_type = ' and '.join(CHAMPS['data'][champion]['tags'])
        champ_name = champ_data['name']
        await ctx.send(f'{champ_name} is a {champ_type}')
        if voice == None:
            return
        elif voice and (voice.is_paused() or voice.is_playing()):
            return
        else:
            gTTS(f'{champ_name} is a {champ_type}').save('tts.mp3')
            voice.play(discord.FFmpegPCMAudio("tts.mp3",executable='ffmpeg'))
    except:
        await ctx.send("Unknown champion. Try about [champion]")
'''
@bot.command(name='fr', 
            brief='Checks champion if it\'s on free rotation',
            pass_context = True)
async def fr(ctx, *args):
    if args[-1] == 'unmute':
        voice = get(bot.voice_clients, guild=ctx.guild)
        args = tuple(list(args[:-1]))
    else:
        args = tuple(list(args))
        voice = None
    champion_to_check = "".join([arg.capitalize() for arg in args]).strip()
    try:
        if int(CHAMPS['data'][champion_to_check]['key']) in FREE_ROTATION['freeChampionIds']:
            free_rotation = f'{" ".join([arg.capitalize() for arg in args])} is on free rotation for accounts over level 10'
        else:
            free_rotation = f'{" ".join([arg.capitalize() for arg in args])} is on NOT free rotation'
        await ctx.send(free_rotation)
        if voice == None:
            return
        elif voice and (voice.is_paused() or voice.is_playing()):
            return
        else:
            gTTS(free_rotation).save('tts.mp3')
            voice.play(discord.FFmpegPCMAudio("tts.mp3",executable='ffmpeg'))
    except:
        await ctx.send("Unknown champion. Try about fr [champion]", delete_after=20)
'''
@bot.command(name='tts', 
            brief='tts',
            pass_context = True)
async def tts(ctx, *args):
    msg = " ".join(args)
    voice = get(bot.voice_clients, guild=ctx.guild)
    if ctx.author.id in [645940845245104130]:
        try:
            if voice == None:
                return
            elif voice and (voice.is_paused() or voice.is_playing()):
                return
            else:
                gTTS(msg).save('tts.mp3')
                voice.play(discord.FFmpegPCMAudio("tts.mp3",executable='ffmpeg'))
        except:
            await ctx.send("Unknown error. Try $tts <message>")
'''

bot.run(DISCORD_TOKEN)
