#bot.py

import os
import discord
from secrets import DISCORD_TOKEN

TOKEN = DISCORD_TOKEN
client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild == 'The Alt-Write':
            print(f'{client.user} has connected to Discord!')
            print(f'{guild.name}(id: {guild.id})')

            members = '\n - '.join([member.name for member in guild.members])
            print(f'Guild Members:\n - {members}')

client.run(TOKEN)
