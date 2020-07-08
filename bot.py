#bot.py

import os
import discord

ON_HEROKU = 'ON_HEROKU' in os.environ

if ON_HEROKU == False:
    from secrets import DISCORD_TOKEN
    TOKEN = DISCORD_TOKEN
else:
    TOKEN = os.environ.get('ON_HEROKU')

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    nice_variations = ['nice', 'naisu', 'naice', ]

    for word in nice_variations:
        if word in message.content.strip().lower():
            await message.channel.send('Naisu!')
            await message.channel.send("https://media.giphy.com/media/qPcX2mzk3NmjC/giphy.gif")

client.run(TOKEN)
