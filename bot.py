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


def get_lp(discord_id):
    discord_id = str(discord_id)
    conn = psycopg2.connect(DATABASE_URL, sslmode='require',
                            database=DATABASE, user=USER, password=PASSWORD)
    cursor = conn.cursor()
    cursor.execute(
        """
            SELECT *
            FROM elo_tracker
            WHERE
            discord_id = %s
            """, (discord_id,)
    )

    result = cursor.fetchall()[0]
    division = result[1]
    lp = result[2]
    return division, lp


def lp_win(discord_id):
    discord_id = str(discord_id)
    conn = psycopg2.connect(DATABASE_URL, sslmode='require',
                            database=DATABASE, user=USER, password=PASSWORD)

    cursor = conn.cursor()
    cursor.execute(
        """
            SELECT *
            FROM elo_tracker
            WHERE
            discord_id = %s
            """, (discord_id,)
    )
    result = cursor.fetchall()[0]
    division = result[1]
    lp = result[2]

    lp += random.randint(13, 20)

    if (lp >= 100):

        league_dict = {
            "Iron 4": "Iron 3",
            "Iron 3": "Iron 2",
            "Iron 2": "Iron 1",
            "Iron 1": "Silver 4",
            "Silver 4": "Silver 3",
            "Silver 3": "Silver 2",
            "Silver 2": "Silver 1",
            "Silver 1": "Gold 4",
            "Gold 4": "Gold 4"
        }

        cursor.execute(
            """
            UPDATE elo_tracker
            SET lp = %s, division = %s
            WHERE
            discord_id = %s
            """, (lp, league_dict[division], discord_id)
        )

        conn.commit()
        conn.close()

    else:
        cursor.execute(
            """
                UPDATE elo_tracker
                SET lp = %s
                WHERE
                discord_id = %s
                """, (lp, discord_id)
        )

        conn.commit()
        conn.close()


def lp_lose(discord_id):
    discord_id = str(discord_id)
    conn = psycopg2.connect(DATABASE_URL, sslmode='require',
                            database=DATABASE, user=USER, password=PASSWORD)
    cursor = conn.cursor()
    cursor.execute(
        """
            SELECT *
            FROM elo_tracker
            WHERE
            discord_id = %s
            """, (discord_id,)
    )
    result = cursor.fetchall()[0]
    division = result[1]
    lp = result[2]

    lp -= random.randint(13, 20)

    if (lp <= 0):
        if (division != "Iron"):
            lp = 75

        league_dict = {
            "Iron 4": "Iron 4",
            "Iron 3": "Iron 4",
            "Iron 2": "Iron 3",
            "Iron 1": "Iron 2",
            "Silver 4": "Silver 4",
            "Silver 3": "Silver 4",
            "Silver 2": "Silver 3",
            "Silver 1": "Silver 2",
            "Gold 4": "Gold 4"
        }

        cursor.execute(
            """
            UPDATE elo_tracker
            SET lp = %s, division = %s
            WHERE
            discord_id = %s
            """, (lp, league_dict[division], discord_id)
        )

        conn.commit()
        conn.close()

    else:
        cursor.execute(
            """
                UPDATE elo_tracker
                SET lp = %s
                WHERE
                discord_id = %s
                """, (lp, discord_id)
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
        # print(record)

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database conn.
        if(conn):
            conn.commit()
            cursor.close()
            conn.close()


bot = commands.Bot(command_prefix='wh ')


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

@bot.command()
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

bot.run(TOKEN)
