import os 
import random, requests
import discord
import asyncio
from asyncio import sleep
from discord.ext import commands
#from discord.ui import View, Button
import wavelink
from wavelink.ext import spotify
from modules import (message_handel, channel_handel, config)
from flask import Flask
from threading import Thread
#from discord.ext.commands.converter import (MemberConverter, RoleConverter, TextChannelConverter)

onm = message_handel
ochd = channel_handel
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True
intents.voice_states = True
intents.guilds = True

#Configuring db
pref = config.prefix
maindb = config.maindb

bot = commands.AutoShardedBot(command_prefix= commands.when_mentioned_or(pref), intents=intents) #AutoSharded
bot.remove_command("help")
#support_server = bot.get_guild(config.support_server_id)

async def load_extensions():
	for filename in os.listdir(config.cogs_path):
		if filename.endswith(".py"):
			await bot.load_extension(f"cogs.{filename[:-3]}")
#asyncio.run(load_extensions())

@bot.event
async def on_ready():
	await bot.wait_until_ready()
	await load_extensions()
	try:
		await node_connect()
		await bot.tree.sync()
		stmsg = f'{bot.user} is ready with {len(bot.commands)} commands'
		print(stmsg)
		requests.post(url=config.stwbh, json={"content":"<@885193210455011369>","embeds":[{"title":"Status","description":stmsg,"color":0xff00}]})
		while True:
			for st in config.status:
				await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=st))
				await sleep(120)
	except Exception as ex:
		print(ex)

async def node_connect():
	try:
		await bot.wait_until_ready()
		await wavelink.NodePool.create_node(bot=bot,host=config.m_host,port=443,password=config.m_host_psw,https=True,spotify_client=spotify.SpotifyClient(client_id=config.spot_id,client_secret=config.spot_secret))
	except Exception as e:
		print(e)


#await nitrof(message)
#await onm.auto_grp(message, bot)
@bot.event
async def on_message(message):
	if config.notuser(message):
		return
	await bot.process_commands(message)
	await onm.tourney(message)
	await onm.ask(message, bot=bot)
	
@bot.event
async def on_guild_channel_delete(channel):
    await ochd.ch_handel(channel, bot)
	
@bot.event
async def on_command_error(ctx, error, bot=bot):
    await onm.error_handle(ctx, error, bot=bot)

##########################################################################################
#                                       COMMANDS
############################################################################################

def mmbrs(ctx=None):
    i = 0
    for guild in bot.guilds:
        i = i + guild.member_count
    return i

@bot.hybrid_command(with_app_command = True, aliases=["bi","stats", "about", "info", "status", "botstats"])
@commands.cooldown(2, 60, commands.BucketType.user)
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def botinfo(ctx):
    await ctx.defer(ephemeral=True)
    emb = discord.Embed(title="Spruce Bot", description="Welcome To Spruce", color=discord.Color.blurple())
    mmbs = mmbrs()
    emb.add_field(name=f"{config.servers}__Servers Info__", value=f"Total server : {len(bot.guilds)}\nTotal Members : {mmbs}", inline=False)
    emb.add_field(name=f"{config.developer} __Developer__", value="[Hunter#6967](https://discord.com/users/885193210455011369)", inline=False)
    emb.add_field(name=f"{config.ping} __Current Ping__", value=random.choice(range(19,28)), inline=False)
    emb.add_field(name=f"{config.setting} __Command Prefix__", value=f"command: {pref}help, prefix: {pref}  ", inline=False)
    emb.set_footer(text="Made with ❤️ | By hunter#6967")
    return await ctx.send(embed=emb)

app = Flask('')

@app.route('/')
def home():
    return "bot : spruce#6967"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
keep_alive()

bot.run(config.token)