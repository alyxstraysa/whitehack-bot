#bot.py

import os
import discord
from secrets import DISCORD_TOKEN

TOKEN = DISCORD_TOKEN
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)
