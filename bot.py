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

bot = commands.Bot(command_prefix='!', intents=intents)

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

    nameList=[member.name for member in userlist]
    game=roles.GameState(nameList)
    # game.set_random_roles()

    await send_role(game,ctx)
    print(game.players)
    print("printing game object")
    print(game)
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
    
async def send_role(game,ctx):
    werewolf_list = []
    camper_list = []
    other_list = []
    userlist.pop(0)
    
    for player in game.players:
        print(player.name + " "+ player.get_role_info())
        if player.get_role_info() == "Werewolf":
            for user in userlist:
                if user.name == player.name:
                    werewolf_list.append(user)
        elif player.get_role_info() == "Camper":
            for user in userlist:
                if user.name == player.name:
                    camper_list.append(user)
        elif player.get_role_info() == "Wannabe":
            for user in userlist:
                if user.name == player.name:
                    other_list.append(user)

    print(camper_list)
    for camper in camper_list:
        embed = create_camper_msg()
        channel = await camper.create_dm()
        msg = await channel.send(embed=embed)
        await ctx.send("Your role has been sent %s" %camper.name)
    
    for werewolf in werewolf_list:
        embed = create_werewolf_msg(werewolf_list)
        channel = await werewolf.create_dm()
        msg = await channel.send(embed=embed)
        await ctx.send("Your role has been sent %s" %werewolf.name)
    

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
    await asyncio.sleep(5)
    message = await ctx.channel.fetch_message(message.id)
    reaction = message.reactions[0] # checkmark reactions only
    
    async for user in reaction.users():
            userlist.append(user)
            await ctx.send(user.name) 
    await gameLogic(ctx, 1, 1)

# Set the Settings for number of roles
# Note has a writing error if number error is not at the end
@bot.command(name="settings")
async def set_settings(ctx, *args):

    list_of_roles = ["werewolf", "camp_councellor", "wannabe", "introvert", "bffpair","camper"]
    number_of_each_role = {"werewolf":0, "camp_councellor":0, "wannabe":0, "introvert":0, "bffpair":0, "camper":0}
    
    def check(message):
         return message.author == ctx.author and message.channel == ctx.channel

    if len(args) !=6 :
        await ctx.send("You need **6** arguments. Please enter 6 numbers, each will correspond to the number of each roles to be used during the game\n"
                        + "Do `$settings <num of werewolf> <num of councellor> <num of wannabe> <num of introverts> <num of bffpair> <num of camper>`\n"
                        + "For example: **$settings 1 1 0 0 1 3** for 1 werewolf, 1 councellor, 0 wannabes, 0 introverts, 1 pair of bffs(ie 2 players can have this role), 3 campers. ")
        raise BaseException
    
    NOT_A_NUMBER = 1
    while (NOT_A_NUMBER):
        print(f"The args are: ", args)
        for i in range(6):
            try:
                role_int = int(args[i])
                number_of_each_role[list_of_roles[i]] = role_int
                NOT_A_NUMBER = 0
            except ValueError:
                await ctx.send("Must be a number!\nPlease enter 6 numbers, each will correspond to the number of each role used during the game")
                new_arguments = await bot.wait_for("message",check=check)
                print(f'New arguments are: {new_arguments.content}')
                args = new_arguments.content.split()
                NOT_A_NUMBER = 1
                break

    await ctx.send(f"Set settings successfully.\n" + 
                    "**Werewolves:** " + str(number_of_each_role["werewolf"]) + "\t**CampCounsellor:** " + str(number_of_each_role["camp_councellor"]) +
                    "\t**Wannabe:** "+ str(number_of_each_role["wannabe"]) + "\t**Introvert:** " + str(number_of_each_role["introvert"]) + "\t**Pairs of BFFs:** " + str(number_of_each_role["bffpair"]) +
                    "\t**Campers:** " + str(number_of_each_role["camper"]))
    print(f"New role lmits are: {number_of_each_role}")

################ TESTING POLL ###################
channel_list=[]
@bot.command(name='poll')
async def poll_test(ctx):
    # vote_list = []
    # for user in userlist:
    #     vote_list.append(poll(user.name, 0))

    embed = create_poll(userlist, poll_list)
    #member = ctx.message.author
    userlist.pop(0)
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

@bot.command(name='dmcamper', help='send dm to campers')
async def printlist(ctx):
    camperlist = []

    userlist.pop(0)
    embed = create_camper_msg(userlist)
    for camper in userlist:
        channel = await camper.create_dm()
        msg = await channel.send(embed=embed)
        await ctx.send("Your role has been sent %s" %camper.name)

@bot.command(name='dmwerewolf', help='send dm to werewolves')
async def printlist(ctx):
    werewolflist = []

    userlist.pop(0)
    print(userlist)
    embed = create_werewolf_msg(userlist)
    for werewolf in userlist:
        channel = await werewolf.create_dm()
        msg = await channel.send(embed=embed)
        await ctx.send("Your role has been sent %s" %werewolf.name)

@bot.command(name='dmintrovert', help='send dm to introvert')
async def printlist(ctx):
    userlist.pop(0)
    userlist.pop(0)
    userlist.pop(0)
    embed = create_introvert_msg(userlist)
    for introvert in userlist:
        channel = await introvert.create_dm()
        msg = await channel.send(embed=embed)
        await ctx.send("Your role has been sent %s" %introvert.name)

@bot.command(name='dmbestfriend', help='send dm to bestfriends')
async def printlist(ctx):
    userlist.pop(0)
    embed = create_best_friend_msg(userlist)
    for best_friend in userlist:
        channel = await best_friend.create_dm()
        msg = await channel.send(embed=embed)
        await ctx.send("Your role has been sent %s" %best_friend.name)

@bot.command(name='dmwannabe', help='send dm to wannabe')
async def printlist(ctx):
    userlist.pop(0)
    userlist.pop(0)
    userlist.pop(0)
    embed = create_wannabe_msg(userlist)
    for wannabe in userlist:
        channel = await wannabe.create_dm()
        msg = await channel.send(embed=embed)
        await ctx.send("Your role has been sent %s" %wannabe.name)

def create_camper_msg():
    embed = discord.Embed(
        title = "You are a Camper!",
        description = "You will have a great time at camp if you get rid of any werewolves and don't accidentally kick out a fellow camper. You just want to have fun at camp.",
        color = discord.Color.blue()
    )
    embed.set_image(url='https://i.imgur.com/4AYKSl3.jpg')
    return embed

def create_werewolf_msg(wolf_list):
    names = []
    delimeter = '\n'
    for wolf in wolf_list:
        names.append(wolf.name)
    list_wolves = delimeter.join(names)
    werewolf_str = "Your fellow wolves are:\n" + list_wolves
    embed = discord.Embed(
        title = "You are a Werewolf!",
        description = "You will have a good trip as long as no one from your misunderstood wolf pack gets kicked out.\n\n" + werewolf_str,
        color = discord.Color.red()
    )
    embed.set_image(url='https://i.imgur.com/VP45oFp.jpg')
    return embed

def create_introvert_msg():
    embed = discord.Embed(
        title = "You are an Introvert!",
        description = "You do not like camp, but your mom made you come. You have to figure out a way to go home without her blaming you. You will have a good trip if you get kicked out in the morning.",
        color = discord.Color.gold()
    )
    embed.set_image(url='https://i.imgur.com/UFh7Xsp.jpg')
    return embed

def create_best_friend_msg(userlist):
    best_friend_str = "Your fellow wolf is %s." %userlist[-1]
    embed = discord.Embed(
        title = "You are a Best Friend!",
        description = "You will have a good time at camp if you get rid of any werewolves and don't accidentally get rid of your best friend - who you know isn't a werewolf.\n\n""" + best_friend_str,
        color = discord.Color.blue()
    )
    embed.set_image(url='https://i.imgur.com/wHgG64a.jpg')
    return embed

def create_wannabe_msg(userlist):
    werewolf_str = "Your fellow wolf is %s." %userlist[-1]
    embed = discord.Embed(
        title = "You are a Wannabe!",
        description = "You really want the werewolves to like you... even though they don't know who you are. Your goal is for none of them to get kicked out, even if that means you have to go instead.\n\n" + werewolf_str,
        color = discord.Color.red()
    )
    embed.set_image(url='https://i.imgur.com/XZSDOEU.jpg')
    return embed

def create_camp_counsellor_msg(userlist):
    embed = discord.Embed(
        title = "You are a Camp Counsellor!",
        description = "You will have a good trip if you get rid of any werewolves and don't accidentally get rid of camper. Luckily, you have extra privileges and can figure out who one camper is or who two of the missing ones were.\n\n",
        color = discord.Color.blue()
    )
    embed.set_image(url='https://i.imgur.com/FnS0HP5.jpg')
    return embed

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