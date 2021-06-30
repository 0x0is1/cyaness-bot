import random
from discord.ext.commands.errors import CommandInvokeError, CommandNotFound
import libcyaness, os, discord, json
from discord.ext import commands, tasks

info = {}
REFRESH_TIME=300
last_comic_index=random.randint(39, 5010)
def embed_generator(data):
    embed=discord.Embed(title='Cyanide and happiness', color=0x71368a)
    embed.set_image(url=data)
    embed.set_footer(text=**Memes by explosm.net | 0x0is1**)
    return embed

def enisable_text_channel(channel_id, status):
    global info
    info[str(channel_id)]=status
    with open('info.json', 'w') as filename:
        json.dump(info, filename)

def help_embed():
    embed = discord.Embed(title=format(bot_name), color=0x71368a)
    embed.add_field(
        name="Description:", value="This bot is designed for posting Hindi and English poems automatically on discord.", inline=False)
    embed.add_field(
        name="**Commands:**\n", value="`register` : Command used for registering this channel.\n`deregister` : Command used for deregistering this channel.\n`enable [hindi/english]` : Command used for enabling language of poem in this channel. \n `disable [hindi/english]` : Command used for disabling language of poem in this channel.", inline=False)
    embed.add_field(
        name="Invite: ", value="You can get invite link by typing `invite`")
    embed.add_field(
        name="Source: ", value="You can get source code by typing `source`")
    embed.add_field(
        name="Credits: ", value="You can get credits info by typing `credits`")
    return embed

def invite_embed():
    embed = discord.Embed(title='{} Invite'.format(bot_name),url='https://discord.com/api/oauth2/authorize?client_id=843522585596788747&permissions=51264&scope=bot',
                description='Invite {} on your server.'.format(bot_name), color=0x71368a)
    return embed

def source_embed():
    source_code = 'https://github.com/0x0is1/cyaness-bot'
    embed = discord.Embed(title='cyaness-bot source code',
                          url=source_code,
                          description='Get cyaness-bot Source Code.', color=0x71368a)
    return embed

bot = commands.Bot(command_prefix='!=')
bot.remove_command('help')

@bot.command(name='help')
async def help(ctx):
    embed = help_embed()
    await ctx.send(embed=embed)

@tasks.loop(seconds=REFRESH_TIME)
async def main_fun():
    global info
    global last_comic_index
    data = libcyaness.get_url(last_comic_index)
    last_comic_index+=1
    channel_ids = list(info.keys())
    for channel_id in channel_ids:
        status=info[channel_id]
        if status=='ON':
            embed=embed_generator(data)
            channel_ob = bot.get_channel(int(channel_id))
            try:
                await channel_ob.send(embed=embed)
            except TypeError:pass

@bot.event
async def on_ready():
    global info
    info = json.load(open('info.json', 'r'))
    print('Bot status: Online.')
    main_fun.start()

@bot.command()
async def meme(ctx):
    data=libcyaness.get_url(random.randint(39, 5010))
    embed=embed_generator(data)
    await ctx.send(embed=embed)

@bot.command()
async def invite(ctx):
    embed = invite_embed()
    await ctx.send(embed=embed)

@bot.command()
async def source(ctx):
    embed = source_embed()
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    await ctx.send('Pong! `{}ms`'.format(round(bot.latency * 1000)))

@bot.command()
async def credits(ctx):
    embed = discord.Embed(title=format(bot_name), color=0x71368a)
    embed.add_field(name='Disclaimer', value='These contents are provided by `explosm.net`.\nWe do not claim any site related property.\nWe do not promote any illegal use of this API/Bot.', inline=False)
    embed.add_field(name='Developer', value='0x0is1', inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def status(ctx):
    global info
    channel_id = ctx.message.channel.id
    channels = info
    channel_ids = list(channels.keys())
    if str(channel_id) in channel_ids:
        embed = discord.Embed(color=0x71368a)
        s=channels[str(channel_id)]
        embed.add_field(name='Status:', value=s, inline=False)
        await ctx.send(embed=embed)

@bot.command()
async def enable(ctx):
    channel_id = ctx.message.channel.id
    enisable_text_channel(channel_id, 'ON')
    await ctx.message.add_reaction('✅')

@bot.command()
async def disable(ctx):
    channel_id = ctx.message.channel.id
    enisable_text_channel(channel_id, 'OFF')
    await ctx.message.add_reaction('✅')

@bot.command()
async def deregister(ctx):
    channel_id = ctx.message.channel.id
    channels = json.load(open('info.json', 'r'))
    channel_ids = list(channels.keys())
    if str(channel_id) in channel_ids:
        global info
        info.pop(str(channel_id))
        with open('info.json', 'w') as filename:
            json.dump(info, filename)
        embed = discord.Embed(color=0x71368a)
        embed.add_field(name='Info: ',
                        value='This text channel is no more subscribed. \n Use `register` command to resubscribe.', inline=False)
        await ctx.send(embed=embed)

@bot.command()
async def register(ctx):
    channel_id = ctx.message.channel.id
    channels = json.load(open('info.json', 'r'))
    channel_ids = list(channels.keys())
    if not str(channel_id) in channel_ids:
        global info
        info[str(channel_id)] = []
        info[str(channel_id)].append('OFF')
        with open('info.json', 'w') as filename:
            json.dump(info, filename)
        embed = discord.Embed(color=0x71368a)
        embed.add_field(name='Info: ', value='This channel is subscribed now. \n Use `enable` or `disable` commands to interact.\n Or use `deregister` command to unsubscribe.', inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send(message='This channel is already registered.')

@disable.error
async def disable_error(ctx, error):
    await ctx.send('`Channel is not registered. Please use register command to register.`')
    print(error)

@enable.error
async def enable_error(ctx, error):
    await ctx.send('`Channel is not registered. Please use register command to register.`')
    print(error)

@register.error
async def register_error(ctx, error):
    await ctx.send('`Channel might be already registered.`')
    print(error)

@deregister.error
async def deregister_error(ctx, error):
    await ctx.send('`Channel might not be already registered.`')
    print(error)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send('`Unknown command` \n Please use right command to operate. `help` for commands details.')
    if isinstance(error, CommandInvokeError):
        return
    if isinstance(error, discord.errors.HTTPException):
        return
    print(error)

auth_token = os.environ.get('EXPERIMENTAL_BOT_TOKEN')
bot.run(auth_token)
