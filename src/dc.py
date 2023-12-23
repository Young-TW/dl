import discord
from discord.ext import commands
import asyncio
import json

with open('setting.json', mode='r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

intents = discord.Intents.all()
bot=commands.Bot(command_prefix=".",intents=intents)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    game = discord.Game("Discord")
    await bot.change_presence(status=discord.Status.idle, activity=game)

@bot.command()
async def ping(ctx):
    await ctx.send(f'{round(bot.latency*1000)}ms')

@bot.command()
async def scan(ctx, channel_id: int):
    channel = bot.get_channel(channel_id)
    messages = channel.history(limit=100)
    urls = ""
    async for message in messages:
        if message.content.startswith('https://85tube.com/videos/'):
            urls += (message.content + '\n')
            print(message.content)
        else:
            print('not match')

    await ctx.send(urls)
    print('done')

@bot.command()
async def scan_channel(ctx, channel: discord.TextChannel):
    await ctx.send(f'Channel Name: {channel.name}\nChannel ID: {channel.id}')

@bot.command()
@commands.is_owner()
async def delete(ctx:commands.Context,number:int):
    await ctx.channel.purge(limit=number+1)

bot.run(jdata['BotTOKEN'])