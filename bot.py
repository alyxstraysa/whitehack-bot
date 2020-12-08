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

    elif "BANNED" == message.content:
        await message.channel.send("https://i.imgur.com/rarpoUg.mp4")

    elif "iron" == message.content:
        await message.channel.send("You mean elo heaven?")

    elif re.search(r'wa+h', message.content) is not None:
        await message.channel.send("https://tenor.com/view/dance-waluigi-mario-meme-gif-5329543")

    elif re.search(r'WA+H', message.content) is not None:
        await message.channel.send("https://tenor.com/view/dance-waluigi-mario-meme-gif-5329543")

    elif "awoo" in message.content.lower():
        await message.channel.send("https://i3.kym-cdn.com/photos/images/original/000/910/542/1e8.jpg")

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

    await bot.process_commands(message)

#define cogs
class anime_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
                    r = requests.get("https://api.jikan.moe/v3/anime/{anime_id}".format(anime_id=anime_id))
                    print(r.text)

        embed = discord.Embed(title="Anime Recommendation")
        embed.add_field(name="Name", value=anime['title'])
        embed.add_field(name="Description", value=anime['synopsis'][0:1000])

        print(anime['synopsis'])

        embed.set_image(url=anime['image_url'])

        await ctx.send(embed=embed)

bot.add_cog(anime_cog(bot))

@bot.command(brief='Send to horny jail', description='Bonks a degenerate in need of bonking')
async def bonk(ctx, username):
    await ctx.send("https://i.imgur.com/t1a9akh.gif")

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

@bot.command(brief='Rolls a 20 sided dice', description='Rolls a twenty sided dice')
async def diceroll(ctx):

    dice_roll = random.randint(1, 20)

    embed = discord.Embed()
    embed.add_field(name="Roll", value=dice_roll)

    await ctx.send(embed=embed)


## league inhouse commands
# function to check league username
async def check_username(username):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{username}?api_key={rito_api_token}".format(username=username, rito_api_token=rito_api_token)) as r:
            if r.status == 200:
                return True
            else:
                return False

            
@bot.command(description='Sends the date of the next inhouse')
async def inhouse_nextgame(ctx):
    await ctx.send("The next inhouse is 12/5/2020! Hope to see you there!")

@bot.command(description='Shows the inhouse leaderboard.')
async def inhouse_leaderboard(ctx):
    await ctx.send("TheYelloBoi has the most wins with 1000 wins.")

    await ctx.send("SkyPangoro has the most kills with 1000 kills.")

    await ctx.send("CornTurtle8 is the biggest animale and the winner of the Catto Award.")

@bot.command(description='Register for the inhouse. Requires two arguments, your League username and your role (ADC, Mid, Support, Top, Jungle).')
async def inhouse_register(ctx, username, role):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require',
                            database=DATABASE, user=USER, password=PASSWORD)
    cursor = conn.cursor()

    #check if user in database
    cursor.execute(
            """
            SELECT * from participant_info
            where discord_id = (%s)
            """,
            (ctx.message.author.id,)
    )
    
    if role not in ['ADC', 'Mid', 'Support', 'Top', 'Jungle', 'Dog']:
        await ctx.send("Sorry, we don't recognize that role.")
        return

    if len(cursor.fetchall()) > 0:
        await ctx.send("Sorry, it looks like you've already registered for the inhouse.")
    else:
        valid = check_username(username)
        if valid:
            cursor.execute(
                """
                INSERT INTO participant_info VALUES
                    (%s, %s, %s)
                ;
                """,
                (username, role, ctx.message.author.id)
            )
            await ctx.send("Thank you for registering!")
            
        else:
            await ctx.send("Sorry, but we can't find that league username!")
                    
    conn.commit()
    conn.close()


#implement method to change league name bound to your ID
@bot.command(description='Change your League username to something else in the inhouse.')
async def inhouse_changeid(ctx, username):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require',
                            database=DATABASE, user=USER, password=PASSWORD)
    cursor = conn.cursor()
    
    valid = check_username(username)
    if valid:
        #check if user in database
        cursor.execute(
            """
            UPDATE participant_info
            SET league_name = (%s)
            where discord_id = (%s)
            """,
            (username, ctx.message.author.id)
        )
        await ctx.send("League name updated!")
    
    else:
        await ctx.send("Sorry, but we can't find that league username!")

    conn.commit()
    conn.close()
    

@bot.command()
async def inhouse_userinfo(ctx, member: discord.Member = None):
    user_id = member.id or ctx.author.id
    conn = psycopg2.connect(DATABASE_URL, sslmode='require',
                            database=DATABASE, user=USER, password=PASSWORD)

    cursor = conn.cursor()
    cursor.execute(
            """
            SELECT * from participant_info
            where discord_id = (%s)
            """,
            (user_id,)
    )
    results = cursor.fetchall()

    if len(results) == 0:
        await ctx.send("There is no user registered with that account.")
        return
    else:
        embed = discord.Embed()
        embed.add_field(name="League ID", value=results[0][0], inline=False)
        embed.add_field(name="Role ID", value=results[0][1], inline=False)

        await ctx.send(embed=embed)

    conn.commit()
    conn.close()


#making fun of jonathan commands
@bot.command(brief='Checks Fetri\'s current LP', description='Calls the Riot API to fetch Fetri\'s current LP and Elo')
async def isjtdiamondyet(ctx):
    
    async with aiohttp.ClientSession() as session:
        # async with session.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/Fetri?api_key={rito_api_token}".format(rito_api_token=rito_api_token)) as r:
        #     if r.status == 200:
        #         user = await r.json()
        #         accountId = user['id']
               
        async with session.get("https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/jlKbXhBN5wSlfLzlLyGggV6W7PBJRULgC9__LMhtOuI9Roc?api_key={rito_api_token}".format(rito_api_token=rito_api_token)) as r:
            if r.status == 200:
                user_info = await r.json()

    if user_info[0]['tier'] == "DIAMOND":
        await ctx.send("He has reached the promise land!")
    else:
        await ctx.send("Crittlestick's current rank is {tier} : {rank}".format(tier=user_info[0]['tier'], rank=user_info[0]['rank']))
        
bot.run(TOKEN)
