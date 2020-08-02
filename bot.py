# bot.py

import os
import discord
import requests
from discord.ext import commands
import aiohttp
import psycopg2
import random
import re

ON_HEROKU = 'ON_HEROKU' in os.environ

if ON_HEROKU == False:
    from secrets import DISCORD_TOKEN, rito_api_token, USER, PASSWORD, DATABASE_URL, DATABASE
    TOKEN = DISCORD_TOKEN

else:
    TOKEN = os.environ.get('TOKEN')
    rito_api_token = os.environ.get('RITO_API_TOKEN')
    USER = os.environ.get('USER')
    PASSWORD = os.environ.get('PASSWORD')
    DATABASE = os.environ.get("DATABASE")
    DATABASE_URL = os.environ.get('DATABASE_URL')

bot = commands.Bot(command_prefix='wh ')

bot.description = "RPG management tool for the Whitehack RPG as well as various memes."


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # if message.author ==

    nice_variations = ['nice', 'naisu', 'naice', ]

    for word in nice_variations:
        if word in message.content.strip().lower():
            await message.channel.send("Naisu!")

    if "JT" in message.content:
        await message.channel.send("You mean professional jungler WingedNinja2?")

    elif "Justin" in message.content:
        await message.channel.send("Tarkov is not a real game.")

    elif "iron" in message.content:
        await message.channel.send("You mean elo heaven?")

    elif re.search(r'wa+h', message.content) is not None:
        await message.channel.send("https://tenor.com/view/dance-waluigi-mario-meme-gif-5329543")

    elif re.search(r'WA+H', message.content) is not None:
        await message.channel.send("https://tenor.com/view/dance-waluigi-mario-meme-gif-5329543")

    elif "yes" in message.content.lower():
        await message.channel.send("https://imgur.com/l5irxe8")

    await bot.process_commands(message)

@bot.command(brief='Shows the requested Whitehack Character', description='Returns a registered www.praisethetsun.com Whitehack character if one such character is registered')
async def character(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://mysterious-tor-57369.herokuapp.com/api/characters") as r:
            if r.status == 200:
                character = await r.json()

    embed = discord.Embed(title="Whitehack Character",
                          url="http://www.praisethetsun.com")

    embed.add_field(name="Character Name", value=character[0]['charactername'])
    embed.add_field(name="Class", value=character[0]['characterclass'])
    embed.add_field(name="Level", value=character[0]['characterlevel'])

    print(ctx.message.author.id)
    await ctx.send(embed=embed)

@bot.command(brief='Recommends a random anime', description='Returns a carefully curated list of anime for non-plebs.')
async def recommend_anime(ctx):
    anime_id_list = [
        "13125",
        "10721",
        "9756"
    ]

    anime_id = random.choice(anime_id_list)

    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.jikan.moe/v3/anime/{anime_id}".format(anime_id = anime_id)) as r:
            if r.status == 200:
                anime = await r.json()

    embed = discord.Embed(title="Anime Recommendation")
    embed.add_field(name="Name", value=anime['title'])
    embed.add_field(name="Description", value=anime['synopsis'])

    print(anime['synopsis'])

    embed.set_image(url=anime['image_url'])

    await ctx.send(embed=embed)

bot.run(TOKEN)
