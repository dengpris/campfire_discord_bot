# bot.py
from operator import mod
import os
import random
import asyncio

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

@bot.command(name='timer', help='timer command. usage !timer <num of minutes>')
async def timer(ctx, minutes):
    try:
        minuteint = int(minutes)
        totalseconds=minuteint*60
        if minuteint > 60:
            await ctx.send("I dont think im allowed to do go above 60 minutes.")
            raise BaseException
        if minuteint <= 0:
            await ctx.send("I dont think im allowed to do negatives")
            raise BaseException
        
        message = await ctx.send("Timer: {minuteint} minutes")
        while True:
            totalseconds -= 1
            if totalseconds == 0:
                await message.edit(content="Ended!")
                break
            minuteLeft=totalseconds//60
            secondsLeft=totalseconds%60
            await message.edit(content=f"Timer: {minuteLeft} minutes {secondsLeft} seconds")
            await asyncio.sleep(1)
        await ctx.send(f"{ctx.author.mention} Your countdown Has ended!")
    except ValueError:
        await ctx.send("Must be a number!")

################# JOIN FUNCTIONS ##################
userlist=[]
@bot.command(name='join', help='returns list of people who joined')
async def addlist(ctx):
    member = ctx.message.author.id
    userlist.append(member)
    await ctx.send("<@" + str(member) + ">" + ", you've joined the game!")

@bot.command(name='unjoin', help='unjoin the game')
async def removelist(ctx):
    member = ctx.message.author.id
    userlist.remove(member)
    await ctx.send("<@" + str(member) + ">" + ", you've left the game!")

@bot.command(name='players', help='current players')
async def printlist(ctx):
    await ctx.send("Players: ")
    for member in userlist:
        await ctx.send("<@" + str(member) + ">")

bot.run(TOKEN)