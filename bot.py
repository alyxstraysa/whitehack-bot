#bot.py

import os
import discord
import requests
from discord.ext import commands

ON_HEROKU = 'ON_HEROKU' in os.environ

if ON_HEROKU == False:
    from secrets import DISCORD_TOKEN
    TOKEN = DISCORD_TOKEN
else:
    TOKEN = os.environ.get('TOKEN')
    rito_api_token = os.environ('RITO_API_TOKEN')

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
        await message.channel.send("You mean Tarkov only mid?")

    await bot.process_commands(message)

# @bot.command()
# async def intcheck(ctx, username):
#     await ctx.send("{} is a dirty inter!".format(username))

@bot.command()
async def intcheck(ctx, username):
    r = requests.get("https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/JqUMHMnyZtqXTOJW0RVjNcJ3fvwsOALgXymZ8PvR5pbLKw?endIndex=10&api_key={}".format(rito_api_token)
    )

    match_history = r.json()
    win_counter = 0

    for match in match_history['matches']:
        game_id = match['gameId']
        champion_id = match['champion']
        indiv_hist = requests.get("https://na1.api.riotgames.com/lol/match/v4/matches/{game_id}?api_key={riot_token}".format(game_id=game_id, riot_token=rito_api_token))
        indiv_hist = indiv_hist.json()

        for participant in indiv_hist['participants']:
            if participant['championId'] == champion_id:
                if participant['stats']['win'] == True:
                    win_counter += 1

    await ctx.send("{username} has lost {loss} out of their past 10 games!".format(username=username, loss=(10 - win_counter)))
    
bot.run(TOKEN)
