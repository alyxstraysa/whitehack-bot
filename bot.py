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
@commands.cooldown(1, 4, commands.BucketType.guild)
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

    embed = discord.Embed(title="Anime Recommendation")
    embed.add_field(name="Name", value=anime['title'])
    embed.add_field(name="Description", value=anime['synopsis'][0:1000])

    print(anime['synopsis'])

    embed.set_image(url=anime['image_url'])

    await ctx.send(embed=embed)


@bot.command(brief='Rolls a 20 sided dice', description='Rolls a twenty sided dice')
async def diceroll(ctx):

    dice_roll = random.randint(1, 20)

    embed = discord.Embed()
    embed.add_field(name="Roll", value=dice_roll)

    await ctx.send(embed=embed)


## league commands
@bot.command()
async def intcheck(ctx, username):
    win_counter = 0

    async with aiohttp.ClientSession() as session:
        async with session.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{username}?api_key={rito_api_token}".format(username=username, rito_api_token=rito_api_token)) as r:
            if r.status == 200:
                user = await r.json()
                accountId = user['accountId']

        async with session.get("https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{account_id}?endIndex=10&api_key={rito_api_token}".format(account_id=accountId, rito_api_token=rito_api_token)) as r:
            if r.status == 200:
                match_history = await r.json()

        for match in match_history['matches']:
            game_id = match['gameId']
            champion_id = match['champion']

            async with session.get("https://na1.api.riotgames.com/lol/match/v4/matches/{game_id}?api_key={riot_token}".format(game_id=game_id, riot_token=rito_api_token)) as r:
                if r.status == 200:
                    indiv_hist = await r.json()

                for participant in indiv_hist['participants']:
                    if participant['championId'] == champion_id:
                        if participant['stats']['win'] == True:
                            win_counter += 1

    await ctx.send("{username} has lost {loss} out of their past 10 games!".format(username=username, loss=(10 - win_counter)))

    if (10 - win_counter) > 5:
        await ctx.send("{username} is a dirty inter!".format(username=username))

    if win_counter == 5:
        await ctx.send("{username} is a coinflip player!".format(username=username))


@bot.command()
async def duocheck(ctx, username):
    await ctx.send("You should not duo with {username}".format(username=username))


@bot.command()
async def getlp(ctx):
    try:
        division, lp = get_lp(ctx.message.author.id)
        await ctx.send("Your current division is {} and your current LP is {}.".format(division, lp))
    except:
        await ctx.send("You have not played any games yet!")


@bot.command()
async def leaguematch(ctx):
    online_users = []
    for user in ctx.guild.members:
        if (user.status != discord.Status.offline) and (user.bot == False):
            # if (user.status != discord.Status.offline):
            online_users.append(user.id)

    if len(online_users) >= 10:
        online_users.remove(ctx.message.author.id)
        selected_match = random.sample(online_users, k=9)
        selected_match.append(ctx.message.author.id)

        # create_table()

        for user in selected_match:
            matchmaking(user)

        user1 = ctx.guild.get_member(int(selected_match[0]))
        user2 = ctx.guild.get_member(int(selected_match[1]))
        user3 = ctx.guild.get_member(int(selected_match[2]))
        user4 = ctx.guild.get_member(int(selected_match[3]))
        user5 = ctx.guild.get_member(int(selected_match[4]))
        user6 = ctx.guild.get_member(int(selected_match[5]))
        user7 = ctx.guild.get_member(int(selected_match[6]))
        user8 = ctx.guild.get_member(int(selected_match[7]))
        user9 = ctx.guild.get_member(int(selected_match[8]))
        user10 = ctx.guild.get_member(int(selected_match[9]))

        await ctx.send("""Blue Team: {user1}, {user2}, {user3}, {user4}, {user5} \nRed Team: {user6}, {user7}, {user8}, {user9}, {user10}""".
                       format(user1=user1,
                              user2=user2,
                              user3=user3,
                              user4=user4,
                              user5=user5,
                              user6=user6,
                              user7=user7,
                              user8=user8,
                              user9=user9,
                              user10=user10
                              ))

        kda_list = []
        for i in range(10):
            kills = random.randint(0, 20)
            deaths = random.randint(0, 20)
            assists = random.randint(0, 20)
            kda_list.append(
                "{kills}/{deaths}/{assists}".format(kills=kills, deaths=deaths, assists=assists))

        await ctx.send(""" 
        Results - \n{user1} : {kda1}\n{user2} : {kda2}\n{user3} : {kda3}\n{user4} : {kda4}\n{user5} : {kda5}\n{user6} : {kda6}\n{user7} : {kda7}\n{user8} : {kda8}\n{user9} : {kda9}\n{user10} : {kda10}
        """.format(user1=user1, kda1=kda_list[0],
                   user2=user2, kda2=kda_list[1],
                   user3=user3, kda3=kda_list[2],
                   user4=user4, kda4=kda_list[3],
                   user5=user5, kda5=kda_list[4],
                   user6=user6, kda6=kda_list[5],
                   user7=user7, kda7=kda_list[6],
                   user8=user8, kda8=kda_list[7],
                   user9=user9, kda9=kda_list[8],
                   user10=user10, kda10=kda_list[9]))

        winner = random.choice(['blue', 'red'])

        if (winner == 'blue'):
            for user in [selected_match[0], selected_match[1], selected_match[2], selected_match[3], selected_match[4]]:
                lp_win(user)

            for user in [selected_match[5], selected_match[6], selected_match[7], selected_match[8], selected_match[9]]:
                lp_lose(user)

        if (winner == 'red'):
            for user in [selected_match[0], selected_match[1], selected_match[2], selected_match[3], selected_match[4]]:
                lp_lose(user)

            for user in [selected_match[5], selected_match[6], selected_match[7], selected_match[8], selected_match[9]]:
                lp_win(user)

    else:
        await ctx.send("Not enough users online!")

bot.run(TOKEN)
