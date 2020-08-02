@bot.command(brief='Rolls a 20 sided dice', description='Rolls a twenty sided dice')
async def diceroll(ctx):

    dice_roll = randint(1, 20)

    embed = discord.Embed()
    embed.add_field(name="Roll", value=dice_roll)

    await ctx.send(embed=embed)
