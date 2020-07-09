#bot.py

import os
import discord
import requests
from discord.ext import commands
import aiohttp
import psycopg2
import random

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


def create_table():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require',
                            database=DATABASE, user=USER, password=PASSWORD)
    cursor = conn.cursor()
    cursor.execute(
            """
            DROP TABLE IF EXISTS elo_tracker;

            CREATE TABLE elo_tracker (
                discord_id VARCHAR(50) PRIMARY KEY,
                division VARCHAR(50),
                LP integer
            );
            """
    )
    conn.commit()
    
    conn.close()
    
def matchmaking(user):
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require',
                            database=DATABASE, user=USER, password=PASSWORD)
        cursor = conn.cursor()
        
        data = (user,)
        cursor.execute(
            """
            INSERT INTO elo_tracker (discord_id, division, LP)
            VALUES
                (
                    %s,
                    'Iron 1',
                    0
                ) 
            ON CONFLICT (discord_id) 
            DO NOTHING;
            """,
            data
        )

        cursor.execute(
            """
            SELECT * FROM elo_tracker;
            """
        )
        
        record = cursor.fetchall()
        #print(record)

    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        #closing database conn.
            if(conn):
                conn.commit()
                cursor.close()
                conn.close()
                print("PostgreSQL conn is closed")

bot = commands.Bot(command_prefix='wh ')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    nice_variations = ['nice', 'naisu', 'naice', ]

    for word in nice_variations:
        if word in message.content.strip().lower():
            await message.channel.send("Naisu!")

    if "JT" in message.content:
        await message.channel.send("You mean professional jungler WingedNinja2?")
    
    if "Justin" in message.content:
        await message.channel.send("Tarkov is not a real game.")
    
    if "iron" in message.content:
        await message.channel.send("You mean elo heaven?")

    await bot.process_commands(message)

@bot.command()
async def intcheck(ctx, username):
    win_counter = 0

    async with aiohttp.ClientSession() as session:
        async with session.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{username}?api_key={rito_api_token}".format(username=username,rito_api_token=rito_api_token)) as r:
            if r.status == 200:
                user = await r.json()
                accountId = user['accountId']

        async with session.get("https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{account_id}?endIndex=10&api_key={rito_api_token}".format(account_id = accountId, rito_api_token=rito_api_token)) as r:
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
async def leaguematch(ctx):
    online_users = []
    for user in ctx.guild.members:
        if (user.status != discord.Status.offline) and (user.bot == False):
        #if (user.status != discord.Status.offline):
            online_users.append(user.id)

    if len(online_users) >= 10:
        online_users.remove(ctx.message.author.id)
        selected_match = random.sample(online_users, k=9)
        selected_match.append(ctx.message.author.id)

        create_table()
        
        for user in selected_match:
            matchmaking(user)

        print(selected_match)
        await ctx.send("""Blue Team: {user1}, {user2}, {user3}, {user4}, {user5} \nRed Team: {user6}, {user7}, {user8}, {user9}, {user10}""".
        format(user1 = ctx.guild.get_member(int(selected_match[0])), 
        user2=ctx.guild.get_member(int(selected_match[1])), 
        user3=ctx.guild.get_member(int(selected_match[2])),
        user4 = ctx.guild.get_member(int(selected_match[3])), 
        user5 = ctx.guild.get_member(int(selected_match[4])), 
        user6 = ctx.guild.get_member(int(selected_match[5])), 
        user7 = ctx.guild.get_member(int(selected_match[6])), 
        user8 = ctx.guild.get_member(int(selected_match[7])), 
        user9 = ctx.guild.get_member(int(selected_match[8])), 
        user10 = ctx.guild.get_member(int(selected_match[9]))
        ))

    else:
        await ctx.send("Not enough users online!")

bot.run(TOKEN)
