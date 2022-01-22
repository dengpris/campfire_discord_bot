# bot.py
import os
import random
import asyncio
import roles

from discord.ext import commands
from dotenv import load_dotenv

from poll import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='~', intents=intents)


@bot.command(name='timer', help='timer command. usage !timer <num of minutes> <num of seconds>')
async def timer(ctx, minutes, seconds=0):
    try:
        minuteint = int(minutes)
        secondsint=int(seconds)
        totalseconds=minuteint*60 + secondsint
        if totalseconds > 3600:
            await ctx.send("I dont think im allowed to do go above 60 minutes.")
            raise BaseException
        if totalseconds <= 0:
            await ctx.send("I dont think im allowed to do negatives")
            raise BaseException
        
        message = await ctx.send("Timer: {minuteint} minutes {secondsint} seconds")
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

@bot.command(name='werewolfEnd', help='kill the game')
async def werewolfEnd(ctx):
    await ctx.send("imma kil l myself")

    exit()

async def gameLogic(ctx, minutes, seconds):

    game=roles.GameState()
    game.set_random_roles()
    #night time timer
    await timer(ctx, 0, 30)

    # ensure camp councellor made choices (if applicalble)

    # dm player to remind role and to vote

    # start day time timer
    await timer(ctx, minutes, seconds)

    #players vote on werewolfs

    #timer ends, initialze vote
    player_booted, num_votes = game.tally_votes()

    #determine winners
    

################# JOIN FUNCTIONS ##################
userlist=[]
poll_list=[]

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

#@bot.command(name='players', help='current players')
#async def printlist(ctx):
#    await ctx.send("Players: ")
#    for member in userlist:
#        await ctx.send("<@" + str(member) + ">")

################ START GAME ######################
@bot.command(name='start', help='start the game')
async def reactlist(ctx):
    # Send message React to Join Game then adds a check emoji
    message = await ctx.send("React to join game!")
    await message.add_reaction('✅')

    # Waits 5 seconds for people to react
    await asyncio.sleep(3)
    message = await ctx.channel.fetch_message(message.id)
    reaction = message.reactions[0] # checkmark reactions only
    
    async for user in reaction.users():
            userlist.append(user)
            await ctx.send(user.name) 

# Set the number of werewolves
@bot.command(name="settings")
async def a_command(ctx):
    global times_used
    await ctx.send(f"Please enter number of werewolves")

    # Check if sent by the same author
    def check(werewolf_number):
        return werewolf_number.author == ctx.author and werewolf_number.channel == ctx.channel

    werewolf_number = await bot.wait_for("message",check=check)

    try:
        werewolf_int = int(werewolf_number.content)
        if werewolf_int < 1 :
            await ctx.send("Requires a minimum of 1 werewolf.")
            raise BaseException
        else:
            await ctx.send("You have selected " + werewolf_number.content + " werewolves")
    
    except ValueError:
        print(f'Not a number')
        await ctx.send("Must be a number!")

################ TESTING POLL ###################
channel_list=[]
@bot.command(name='poll')
async def poll_test(ctx):
    # vote_list = []
    # for user in userlist:
    #     vote_list.append(poll(user.name, 0))

    embed = create_poll(userlist, poll_list)
    #member = ctx.message.author

    for user in userlist:
        if user.bot == False: # do not send messages to yourself
            channel = await user.create_dm()
            message = await channel.send(embed=embed)
            channel_list.append(channel)

        # add reactions
            i=0
            while i<len(userlist):
                await message.add_reaction(unicode_letters[i])
                i = i+1

@bot.command(name='tally')
async def tally_votes(ctx):
    poll_list.sort(key=lambda x: x.votes, reverse=True)
    
    eliminated = poll_list[0].user
    eliminated_2 = poll_list[1].user
    number = poll_list[0].votes
    
    for poll in poll_list:
        print(poll.votes)
    
    if (poll_list[0].votes == poll_list[1].votes):
        message = await ctx.send(f"Members: {eliminated}, {eliminated_2} have been voted out with {number} votes.")
    else:
        message = await ctx.send(f"Member: {eliminated} has been voted out with {number}.")

        
@bot.event
async def on_reaction_add(reaction, user):
    if not isinstance(reaction.message.channel, discord.DMChannel): return
    #channel = await user.create_dm()
    # reactions cannot be removed in DMs
    # for reacts in reaction.message.reactions:
    #     # do not delete if made by bot or if emoji was just created
    #     if (user in await reacts.users().flatten() and not user.bot and str(reacts) != str(reaction.emoji)):
    #         await message.remove_reaction(reaction, user)
    for poll in poll_list:
        name = poll.get_name_from_emoji(reaction.emoji)
        if (name): 
            await user.send("You are now voting for: " + reaction.emoji + " " + name)
            poll.votes = poll.votes+1
            print(poll.votes)


@bot.event
async def on_reaction_remove(reaction, user):
    if not isinstance(reaction.message.channel, discord.DMChannel): return
    for poll in poll_list:
        name = poll.get_name_from_emoji(reaction.emoji)
        if (name): 
            await user.send("You are no longer voting for: " + reaction.emoji + " " + name)
            poll.votes = poll.votes-1


@bot.command(name='players', help='current players')
async def printlist(ctx):
    await ctx.send("Players: ")
    for user in userlist:
        await ctx.send(user.name)

################# DIRECT MESSAGE FUNCTIONS ##################

#Direct messages the list of mentions in message.
mentionlist = []
@bot.command(name='dm', help='direct message mentions')
async def on_message(ctx):
    if 'dm' in ctx.message.content:
        mentionlist = ctx.message.mentions
        await ctx.message.channel.send("A DM has been sent to your inboxes!")
        for mention in mentionlist:
            await mention.send("Hi! I'm here!")


bot.run(TOKEN)