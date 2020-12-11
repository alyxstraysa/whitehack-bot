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
class anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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


@bot.group(nanme='inhouse', brief='Command group for inhouses.', description='Command group for CF inhouses.')
async def inhouse(ctx):
	if ctx.invoked_subcommand is None:
		await ctx.send("Try `wh help inhouse` for all subcommands!")


@inhouse.command(description='Sends the date of the next inhouse')
async def nextgame(ctx):
    await ctx.send("The next inhouse is 12/11/2020 and 12/12/2020! Hope to see you there!")

@inhouse.command(description='Shows the inhouse leaderboard.')
async def leaderboard(ctx):
    await ctx.send(
    """
    TheYelloBoi has the most wins with 1000 wins. \n
    SkyPangoro has the most kills with 1000 kills. \n
    CornTurtle8 is the biggest animale and the winner of the Catto Award.
    """
    )

@inhouse.command(description='Register for the inhouse. Requires two arguments, your League username and your role (ADC, Mid, Support, Top, Jungle).')
async def register(ctx, username, role):
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
@inhouse.command(description='Change your League username to something else in the inhouse.')
async def changeid(ctx, username):
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
    

@inhouse.command()
async def userinfo(ctx, member: discord.Member = None):
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

#waifu voting
@bot.group(nanme='waifu', brief='Command group for waifus.', description='Command group for waifus.')
async def waifu(ctx):
	if ctx.invoked_subcommand is None:
		await ctx.send("Try `wh help waifu` for all subcommands!")


@waifu.command(brief='Vote for a waifu', description='Determine the best anime waifu.')
@commands.cooldown(1, 86400, BucketType.member)
async def vote(ctx, *args):
    waifu = " ".join(args[:])
    conn = psycopg2.connect(DATABASE_URL, sslmode='require',
                            database=DATABASE, user=USER, password=PASSWORD)
    cursor = conn.cursor()
    cursor.execute(
            """
            select waifu_name from waifu;
            """
    )

    waifu_list = [name[0] for name in cursor.fetchall()]
    print(waifu_list)

    if waifu not in waifu_list:
        vote.reset_cooldown(ctx)
        await ctx.send("Sorry, we couldn't find your waifu.")
    else:
        cursor.execute(
            """
            UPDATE waifu 
            SET Votes = Votes + 1
            WHERE waifu_name = (%s);
            """,
            (waifu,)
        )
        await ctx.send("Thank you for voting!")

    conn.commit()
    conn.close()

@waifu.command(brief='Shows waifu info', description='Shows waifu info from the respective wikia')
async def info(ctx, *args):
    waifu = " ".join(args[:])
    conn = psycopg2.connect(DATABASE_URL, sslmode='require',
                            database=DATABASE, user=USER, password=PASSWORD)
    cursor = conn.cursor()
    cursor.execute(
            """
            select wikilink from waifu
            where waifu_name = (%s);
            """, (waifu, )
    )

    def create_anime_embedding(anime_webpage):
        page = requests.get(anime_webpage)
        soup = BeautifulSoup(page.content, 'html.parser')

        description = soup.find_all(property="og:description")
        description = str(description)
        description = re.findall(r'"(.*?)"', description)[0]

        image = soup.find_all(property="og:image")
        image = str(image)
        image = re.findall(r'"(.*?)"', image)[0]

        return description, image

    description, image = create_anime_embedding(cursor.fetchone()[0])

    embed = discord.Embed()
    
    embed.add_field(name="Name", value=waifu, inline=False)
    #embed.add_field(name="Description", value=description, inline=False)
    embed.set_image(url=image)

    await ctx.send(embed=embed)

@waifu.command(brief = 'Shows waifu list', description='Shows the waifus you can vote for')
async def list(ctx):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require',
                            database=DATABASE, user=USER, password=PASSWORD)
    cursor = conn.cursor()
    cursor.execute(
            """
            select * from waifu;
            """
    )

    waifus = [waifu for waifu, _, _, _, in cursor.fetchall()]

    msg = """
    ```
    \n
    {wf}
    ```
    """.format(wf="\n\t".join(waifus))

    print(msg)
    await ctx.send(msg)
    conn.commit()
    conn.close()

@waifu.command(brief='Shows waifu leaderboard', description='In the waifu battle, only one person can be the winner.')
async def leaderboard(ctx):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require',
                            database=DATABASE, user=USER, password=PASSWORD)
    cursor = conn.cursor()
    cursor.execute(
            """
            select * from waifu
            order by votes desc
            limit 3;
            """
    )
    
    results = cursor.fetchall()

    embed = discord.Embed()
    
    embed.add_field(name="Name", value=results[0][0], inline=True)
    embed.add_field(name="Anime", value=results[0][1], inline=True)
    embed.add_field(name="Votes", value=results[0][2], inline=True)
    embed.add_field(name="Name", value=results[1][0], inline=True)
    embed.add_field(name="Anime", value=results[1][1], inline=True)
    embed.add_field(name="Votes", value=results[1][2], inline=True)
    embed.add_field(name="Name", value=results[2][0], inline=True)
    embed.add_field(name="Anime", value=results[2][1], inline=True)
    embed.add_field(name="Votes", value=results[2][2], inline=True)

    await ctx.send(embed=embed)

    conn.commit()
    conn.close()

async def nominate(ctx):
    pass

@vote.error
async def vote_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is rate limited, please try again in {:.0f} hours'.format(error.retry_after / 60 / 60)
        await ctx.send(msg)
    else:
        raise error



        
bot.run(TOKEN)
