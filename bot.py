# bot.py
import os
import discord
from discord.ext.commands.cooldowns import BucketType
import requests
from discord.ext import commands
import aiohttp
import psycopg2
import random
from bs4 import BeautifulSoup
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

bot = commands.Bot(command_prefix='ka ')

bot.description = "Karoo-Bot goes quack."


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

    elif "BANNED" == message.content:
        await message.channel.send("https://i.imgur.com/rarpoUg.mp4")

    elif "iron" == message.content:
        await message.channel.send("You mean elo heaven?")

    elif re.search(r'wa+h', message.content) is not None:
        await message.channel.send("https://tenor.com/view/dance-waluigi-mario-meme-gif-5329543")

    elif re.search(r'WA+H', message.content) is not None:
        await message.channel.send("https://tenor.com/view/dance-waluigi-mario-meme-gif-5329543")

    elif "awoo" in message.content.lower():
        await message.channel.send("https://i.imgur.com/8vdjWf2.jpg")

    elif "jojo yes" == message.content.lower():
        await message.channel.send("https://imgur.com/l5irxe8")

    elif "jojo no" == message.content.lower():
        await message.channel.send("https://imgur.com/zJSVH1g")

    elif "bjergface" == message.content.lower():
        await message.channel.send("https://imgur.com/N5Ig96t")

    elif "what?" == message.content:
        await message.channel.send("https://tenor.com/view/requiem-jojo-anime-shocked-giorno-gif-16966671")

    elif "latom" == message.content:
        await message.channel.send("https://i.imgur.com/b8NIxKN.png")

    elif "rerorero" == message.content:
        await message.channel.send("https://media.giphy.com/media/aYVhZCKdtXZSw/giphy.gif")
    
    elif "worse than death" in message.content:
        await message.channel.send("https://media.giphy.com/media/HDoL0CIhb1uoM/giphy.gif")

    elif "EXILE" == message.content.upper():
        await message.channel.send("https://cdn.discordapp.com/attachments/237359545058328577/841791249895653436/take_him_to_brazil.gif")
    
    elif "uselessmiwa" == message.content.lower():
        await message.channel.send("https://i.imgur.com/jdvSUxC.jpg")

    elif "pityroll" == message.content.lower():
        await message.channel.send("https://i.imgur.com/8ehEWKJ.mp4")

    await bot.process_commands(message)

# define cogs


class anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@bot.command(brief='Send to horny jail', description='Bonks a degenerate in need of bonking')
async def bonk(ctx, username):
    await ctx.send("https://i.imgur.com/t1a9akh.gif")

@bot.command(brief='Recommends a random (popular) anime', description='Returns a list of anime for filthy casuals.')
@commands.cooldown(1, 4, commands.BucketType.guild)
async def animerecfilthycasual(ctx):

    async with aiohttp.ClientSession() as session:
        api_call = "http://api.jikan.moe/v3/top/anime/{randint}".format(
            randint=str(random.randint(1, 20)))
        async with session.get(api_call) as r:
            if r.status == 200:
                anime = await r.json()

    anime_id = random.choice(anime['top'])["mal_id"]

    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.jikan.moe/v3/anime/{anime_id}".format(anime_id=anime_id)) as r:
            if r.status == 200:
                anime = await r.json()

    embed = discord.Embed(title="Anime Recommendation")
    embed.add_field(name="Name", value=anime['title'])
    embed.add_field(name="Description", value=anime['synopsis'][0:1000])

    print(anime['synopsis'])

    embed.set_image(url=anime['image_url'])

    await ctx.send(embed=embed)

@bot.command(brief='Returns info about an anime', description='Returns info about an anime')
@commands.cooldown(1, 4, commands.BucketType.guild)
async def animesearch(ctx, anime_name, summary=None):

    async with aiohttp.ClientSession() as session:
        api_call = "https://api.jikan.moe/v3/search/anime?q={anime}&page=1".format(anime=anime_name)
        async with session.get(api_call) as r:
            if r.status == 200:
                anime = await r.json()
                anime = anime['results'][0]

            mal_id = anime['mal_id']

    r = requests.get("https://myanimelist.net/anime/{mal_id}/".format(mal_id=mal_id))
    soup = BeautifulSoup(r.content, features='html.parser')
    synopsis = soup.find('p', itemprop="description").get_text()

    embed = discord.Embed(title="Anime Search")
    embed.add_field(name="Name", value=anime['title'], inline=False)
    embed.add_field(name='Link', value=anime['url'], inline=False)

    embed.set_image(url=anime['image_url'])

    await ctx.send(embed=embed)

    if summary == 'summary':
        await ctx.send("Summary: " + synopsis)

@bot.command(brief='Recommends a random anime', description='Returns a carefully curated list of anime for non-plebs.')
@commands.cooldown(1, 4)
async def animerec(ctx):
    anime_id_list = [
        "13125",
        "10721",
        "9756"
    ]

    anime_id = random.choice(anime_id_list)

    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.jikan.moe/v3/anime/{anime_id}".format(anime_id=anime_id)) as r:
            if r.status == 200:
                anime = await r.json()
            else:
                print("There is an error with the anime API!")
                import requests
                r = requests.get(
                    "https://api.jikan.moe/v3/anime/{anime_id}".format(anime_id=anime_id))
                print(r.text)

    embed = discord.Embed(title="Anime Recommendation")
    embed.add_field(name="Name", value=anime['title'])
    embed.add_field(name="Description", value=anime['synopsis'][0:1000])

    print(anime['synopsis'])

    embed.set_image(url=anime['image_url'])

    await ctx.send(embed=embed)

#implement whitehack rpg commands
class whitehack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@bot.command(brief='Registers your discord username with the Whitehack bot', description='Registers your discord username with the Whitehack bot and assigns you an ID')
async def whitehackregister(ctx):
    
    r = requests.post('https://whitehackchargen.herokuapp.com/users', json={"discord_id": str(ctx.message.author.id),
                                                                            "discord_name": str(ctx.message.author.name)})

    if r.json()['message'] == "User created successfully":
        await ctx.send("User created successfully!")
    else:
        await ctx.send("There was an error registering your user. Please try again later.")

@bot.command(brief='Generates a random character', description='Generates a random character')
async def whitehackrandomchar(ctx, character_name='Placeholder', race=False):
    r = requests.get('https://whitehackchargen.herokuapp.com/generate?discord_id={discord_id}&race={race}'.format(discord_id = str(ctx.message.author.id), race=race))
    random_char = r.json()

    embed = discord.Embed(title="Whitehack Character")
    embed.add_field(name="Name", value=character_name, inline=False)
    embed.add_field(name="Archetype", value=random_char['archetype'],inline=False)
    embed.add_field(name="Group1", value=random_char['group1'],inline=False)
    embed.add_field(name="Group2", value=random_char['group2'],inline=False)
    embed.add_field(name="Group3", value=random_char['group3'],inline=False)
    embed.add_field(name="Group4", value=random_char['group4'],inline=False)
    embed.add_field(name="Group5", value=random_char['group5'],inline=False)
    embed.add_field(name="Strength", value=random_char['stat_str'],inline=True)
    embed.add_field(name="Dexterity", value=random_char['stat_dex'],inline=True)
    embed.add_field(name="Constitution", value=random_char['stat_con'],inline=True)
    embed.add_field(name="Intelligence", value=random_char['stat_int'],inline=True)
    embed.add_field(name="Wisdom", value=random_char['stat_wis'],inline=True)
    embed.add_field(name="ST", value=random_char['ST'],inline=True)
    embed.add_field(name="HP", value=random_char['HP'],inline=True)
    embed.add_field(name="AC", value=random_char['AC'],inline=True)
    embed.add_field(name="MV", value=random_char['MV'],inline=True)
    embed.add_field(name="AV", value=random_char['AV'],inline=True)    

    await ctx.send(embed=embed)
    await ctx.send("If you would like to save this character, react to this message.")

    try:
        await bot.wait_for('reaction_add', timeout=30, check=lambda reaction, user: reaction.message.id == ctx.message.id and user.id == ctx.message.author.id)
        print("Reacted!")
        #implement post method if they want to save the character

    except:
        pass

bot.run(TOKEN)
