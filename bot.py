# bot.py
from calendar import c
import os
from pickle import FALSE
import random
import asyncio
from tabnanny import check
import roles

from discord.ext import commands
from dotenv import load_dotenv
from discord.utils import get

from poll import *


#GLOBAL VARIABLES
NUM_OF_EACH_ROLE = {"Werewolf":0, "Camp Counselor":0, "Wannabe":0, "Introvert":0, "bffpair":0, "Camper":0}
CUSTOM_ROLES = False

#Default MAXIMUM role values per each number (Note cannot play with 3 players or less)
ROLE_MAX_LIMITS = { "3": {"Werewolf":1, "Camp Counselor":0, "Wannabe":1, "Introvert":1, "bffpair":0, "Camper":2},
                    "4": {"Werewolf":1, "Camp Counselor":1, "Wannabe":1, "Introvert":1, "bffpair":0, "Camper":3},
                    "5": {"Werewolf":2, "Camp Counselor":1, "Wannabe":1, "Introvert":1, "bffpair":0, "Camper":3},
                    "6": {"Werewolf":2, "Camp Counselor":2, "Wannabe":1, "Introvert":1, "bffpair":1, "Camper":4},
                    "7": {"Werewolf":3, "Camp Counselor":2, "Wannabe":2, "Introvert":1, "bffpair":1, "Camper":5},
                    "8": {"Werewolf":3, "Camp Counselor":2, "Wannabe":2, "Introvert":1, "bffpair":1, "Camper":5},
                    "9": {"Werewolf":4, "Camp Counselor":2, "Wannabe":2, "Introvert":1, "bffpair":1, "Camper":6},
                    "10": {"Werewolf":4, "Camp Counselor":2, "Wannabe":2, "Introvert":1, "bffpair":1, "Camper":7}}

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


####### GLOBAL VARIABLES #########
channel_list=[]
userlist=[]
poll_list=[]
player_list=[]
werewolf_list = []
camper_list = []
wannabe_list = []
introvert_list = []
best_friend_list = []
camp_counselor_list = []

#################################
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

###### ASK FOR ROLE SETTINGS HERE 
def create_welcome_camper_msg(role_list):
    embed = discord.Embed(
        title = "Welcome to the CAMP!",
        description = "These are the list of roles!\n\n **Note:** Not all roles may be used during this game session!\n\n" + role_list,
        color = discord.Color.blue()
    )
    embed.set_image(url='https://i.imgur.com/OPCZSjx.png')
    return embed

def settings_usage_text():
    return "You need **6** arguments. Please enter 6 numbers, each will correspond to the number of each roles to be used during the game\n" + "Do `<num of werewolf> <num of Counselor> <num of wannabe> <num of introverts> <num of bffpair> <num of camper>`\n" + "For example: **1 1 0 0 1 3** for 1 werewolf, 1 Counselor, 0 wannabes, 0 introverts, 1 pair of bffs(ie 2 players can have this role), 3 campers."

def set_start_settings(custom_role_numbers):
    list_of_roles = ["Werewolf", "Camp Counselor", "Wannabe", "Introvert", "bffpair","Camper"]
    number_of_each_role =  {"Werewolf":0, "Camp Counselor":0, "Wannabe":0, "Introvert":0, "bffpair":0, "Camper":0}
    for i in range(6):
            role_int = int(custom_role_numbers[i])
            number_of_each_role[list_of_roles[i]] = role_int
    global NUM_OF_EACH_ROLE
    NUM_OF_EACH_ROLE = number_of_each_role
    print("NUM OF EACH ROLE", NUM_OF_EACH_ROLE)
    global CUSTOM_ROLES
    CUSTOM_ROLES = True

async def show_current_roles(ctx, num_players, custom_roles=False):
    
    num_players = 3
    if num_players < 3:
        await ctx.send("Not enough players... maybe find more friends?")
        #exit()
    
    if not custom_roles:
        if num_players > 10:
            num_players = 10
        
        max_num_roles = ROLE_MAX_LIMITS[str(num_players)] 
        role_list = "Current Number of Each Role: \n" + "**Werewolves:** " + str(max_num_roles["Werewolf"]) + "\t\n**Camp Counselor:** " + str(max_num_roles["Camp Counselor"]) + "\t\n**Wannabe:** "+ str(max_num_roles["Wannabe"]) + "\t\n**Introvert:** " + str(max_num_roles["Introvert"]) +  "\t\n**Pairs of BFFs:** " + str(max_num_roles["bffpair"]) + "\t\n**Campers:** " + str(max_num_roles["Camper"]) +  "\n\nPlease remember that not all roles may be used during this game session!" 
    
        embed = create_welcome_camper_msg(role_list)
        await ctx.send(embed=embed)

    await ctx.send("Do you want to customize roles? please enter **y** or **n**")

    def check_y_n(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and \
        msg.content.lower() in ["y", "n"]

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel 

    msg = await bot.wait_for("message", check=check_y_n)
    if msg.content.lower() == "y":
        await ctx.send("**You said yes!**\n" + settings_usage_text())
        custom_role_numbers = await bot.wait_for("message",check=check)
        custom_role_numbers = custom_role_numbers.content.split()
        print(f"Custom_role_numbers is: {custom_role_numbers} with length {len(custom_role_numbers)}")
        while len(custom_role_numbers)!=6:
            await ctx.send(settings_usage_text())
            custom_role_numbers = await bot.wait_for("message",check=check)
            custom_role_numbers = custom_role_numbers.content.split()

        NOT_A_NUMBER = 1
        while (NOT_A_NUMBER):    
            print(f"The args are: ", custom_role_numbers)
            for i in range(6):
                try:
                    int(custom_role_numbers[i])
                except ValueError:
                    await ctx.send("Must be a number!")
                    custom_role_numbers = await bot.wait_for("message",check=check)
                    print(f'New arguments are: {custom_role_numbers.content}')
                    custom_role_numbers = custom_role_numbers.content.split()
                    NOT_A_NUMBER = 1
                    break
            NOT_A_NUMBER = 0

        print("WE'RE HERE!!!! ")
        set_start_settings(custom_role_numbers)
        await ctx.send("DONE CUSTOM")

    else:
        await ctx.send("Alright! Let the Games BEGIN!!!")



async def gameLogic(ctx, minutes, seconds, custom_roles=False):

    nameList=[member.name for member in userlist]
    print(nameList)

    #number of players
    num_players = len(nameList)
    await show_current_roles(ctx, num_players,custom_roles)

    roles_dictionary = NUM_OF_EACH_ROLE
    game=roles.GameState(nameList, roles_dictionary, custom_roles=custom_roles)
    # game.set_random_roles()

    await send_role(game,ctx)
    print(game.players)
    print("printing game object")
    print(game)
    #night time timer
    await timer(ctx, 0, 5)

    # ensure camp Counselor made choices (if applicalble)

    # dm player to remind role and to vote

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
    # start day time timer
    await timer(ctx, 0, 5)

    #players vote on werewolfs
    poll_list.sort(key=lambda x: x.votes, reverse=True)
    
    eliminated = []
    highest_votes = poll_list[0].votes
    print(f"highest votes {highest_votes}")
    for poll in poll_list:     
        if poll.votes == highest_votes:
            print(poll.user)
            for player in player_list:
                elim_player = player.find_player(poll.user)
                if elim_player:
                    eliminated.append(elim_player)
        else:
            break

    for player in eliminated:
        await ctx.send(f"{player.name} has been voted out with {highest_votes} votes.")

    await win_conditions(ctx, eliminated)

    #timer ends, initialze vote
    #player_booted, num_votes = game.tally_votes()

    #determine winners
    
async def send_role(game,ctx):


    for player in game.players:
        player_list.append(roles.Player(player.name, player.get_role_info()))
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
                    wannabe_list.append(user)
        elif player.get_role_info() == "Introvert":
            for user in userlist:
                if user.name == player.name:
                    introvert_list.append(user)
        elif (player.get_role_info() == "bff_1" or player.get_role_info() == "bff_2"):
            for user in userlist:
                if user.name == player.name:
                    best_friend_list.append(user)
        else: #camp_counselor
            for user in userlist:
                if user.name == player.name:
                    camp_counselor_list.append(user)

    for camper in camper_list:
        embed = create_camper_msg()
        if not camper.bot:
            channel = await camper.create_dm()
            msg = await channel.send(embed=embed)
            await ctx.send("Your role has been sent %s!" %camper.name)
    
    for werewolf in werewolf_list:
        embed = create_werewolf_msg(werewolf_list)
        if not werewolf.bot:
            channel = await werewolf.create_dm()
            msg = await channel.send(embed=embed)
            await ctx.send("Your role has been sent %s!" %werewolf.name)    

    for wannabe in wannabe_list:
        embed = create_wannabe_msg(werewolf_list)
        if not wannabe.bot:
            channel = await wannabe.create_dm()
            msg = await channel.send(embed=embed)
            await ctx.send("Your role has been sent %s!" %wannabe.name)
    
    for introvert in introvert_list:
        embed = create_introvert_msg()
        if not introvert.bot:
            channel = await introvert.create_dm()
            msg = await channel.send(embed=embed)
            await ctx.send("Your role has been sent %s!" %introvert.name)

    for best_friend in best_friend_list:
        embed = create_best_friend_msg(best_friend_list)
        if not best_friend.bot:
            channel = await best_friend.create_dm()
            msg = await channel.send(embed=embed)
            await ctx.send("Your role has been sent %s!" %best_friend.name)
    
    

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
    userlist.pop(0)
    await gameLogic(ctx, 1, 1, CUSTOM_ROLES)


################ ROLE SETTINGS ######################
# Set the Settings for number of roles
# Note has a writing error if number error is not at the end

@bot.command(name="settings", help='Set a custom number of each role, run !settings to see usage')
async def set_settings(ctx, *args):

    list_of_roles = ["Werewolf", "Camp Counselor", "Wannabe", "Introvert", "bffpair","Camper"]
    number_of_each_role =  {"Werewolf":0, "Camp Counselor":0, "Wannabe":0, "Introvert":0, "bffpair":0, "Camper":0}
    
    def check(message):
         return message.author == ctx.author and message.channel == ctx.channel

    if len(args) !=6 :
        await ctx.send("You need **6** arguments. Please enter 6 numbers, each will correspond to the number of each roles to be used during the game\n"
                        + "Do `$settings <num of werewolf> <num of Counselor> <num of wannabe> <num of introverts> <num of bffpair> <num of camper>`\n"
                        + "For example: **$settings 1 1 0 0 1 3** for 1 werewolf, 1 Counselor, 0 wannabes, 0 introverts, 1 pair of bffs(ie 2 players can have this role), 3 campers. ")
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
                    "**Werewolves:** " + str(number_of_each_role["Werewolf"]) + "\t**CampCounsellor:** " + str(number_of_each_role["Camp Counselor"]) +
                    "\t**Wannabe:** "+ str(number_of_each_role["Wannabe"]) + "\t**Introvert:** " + str(number_of_each_role["Introvert"]) + "\t**Pairs of BFFs:** " + str(number_of_each_role["bffpair"]) +
                    "\t**Campers:** " + str(number_of_each_role["Camper"]))
    print(f"New role lmits are: {number_of_each_role}")
    global NUM_OF_EACH_ROLE
    NUM_OF_EACH_ROLE = number_of_each_role
    global CUSTOM_ROLES
    CUSTOM_ROLES = True

@bot.command(name="see_roles", help='see current custom role number settings (note that default will set all to 0)')
async def see_settings_roles(ctx):
    #await ctx.send("HERE")
    await ctx.send("Current Number of Each Role: \n" + 
                    "**Werewolves:** " + str(NUM_OF_EACH_ROLE["Werewolf"]) + "\t**CampCounsellor:** " + str(NUM_OF_EACH_ROLE["Camp Counselor"]) +
                    "\t**Wannabe:** "+ str(NUM_OF_EACH_ROLE["Wannabe"]) + "\t**Introvert:** " + str(NUM_OF_EACH_ROLE["Introvert"]) + 
                    "\t**Pairs of BFFs:** " + str(NUM_OF_EACH_ROLE["bffpair"]) + "\t**Campers:** " + str(NUM_OF_EACH_ROLE["Camper"]))

@bot.command(name="reset_roles", help='reset the roles to have default values')
async def see_settings_roles(ctx):
    #await ctx.send("HERE")
    global CUSTOM_ROLES
    CUSTOM_ROLES = False
    global NUM_OF_EACH_ROLE
    NUM_OF_EACH_ROLE = {"Werewolf":0, "Camp Counselor":0, "Wannabe":0, "Introvert":0, "bffpair":0, "Camper":0}
    ## Wrong information
    await ctx.send("**ROLES HAVE BEEN RESET TO DEFAULT VALUES**.\n" +
                    "**If less than or equal to 5 players:**\t1 werewolf, 4 or less campers.\n" + 
                    "**If 6 players:**\t2 werewolf, 1 wannabe, 1 introvert, 1 camp Counselor, 1 camper\n" + 
                    "**If 7 or more players:**\t2 werewolf, 1 wannabe, 1 introvert, 1 camp Counselor, 2 or more campers")
################ TESTING POLL ###################
# channel_list=[]
# @bot.command(name='poll')
# async def poll_test(ctx):
#     # vote_list = []
#     # for user in userlist:
#     #     vote_list.append(poll(user.name, 0))

#     embed = create_poll(userlist, poll_list)
#     #member = ctx.message.author
#     userlist.pop(0)
#     for user in userlist:
#         if user.bot == False: # do not send messages to yourself
#             channel = await user.create_dm()
#             message = await channel.send(embed=embed)
#             channel_list.append(channel)

#         # add reactions
#             i=0
#             while i<len(userlist):
#                 await message.add_reaction(unicode_letters[i])
#                 i = i+1

# @bot.command(name='tally')
# async def tally_votes(ctx):
#     poll_list.sort(key=lambda x: x.votes, reverse=True)
    
#     eliminated = poll_list[0].user
#     eliminated_2 = poll_list[1].user
#     number = poll_list[0].votes
    
#     for poll in poll_list:
#         print(poll.votes)
    
#     if (poll_list[0].votes == poll_list[1].votes):
#         message = await ctx.send(f"Members: {eliminated}, {eliminated_2} have been voted out with {number} votes.")
#     else:
#         message = await ctx.send(f"Member: {eliminated} has been voted out with {number}.")

        
@bot.event
async def on_reaction_add(reaction, user):
    # make sure this is in DMs
    if not isinstance(reaction.message.channel, discord.DMChannel): return

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


############################

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

@bot.event
async def on_reaction_choose(ctx):
    print("herherherherehherherher")
    if not isinstance(ctx.message.channel, discord.DMChannel): return
    #channel = await user.create_dm()
    # reactions cannot be removed in DMs
    # for reacts in reaction.message.reactions:
    #     # do not delete if made by bot or if emoji was just created
    #     if (user in await reacts.users().flatten() and not user.bot and str(reacts) != str(reaction.emoji)):
    #         await message.remove_reaction(reaction, user)

    print(ctx.message.emoji)
    if(ctx.message.emoji == unicode_letters[0]):
        print("emji 0")
    else:
        print("emoji1")
    # for poll in poll_list:
    #     name = poll.get_name_from_emoji(reaction.emoji)
    #     if (name): 
    #         await user.send("You are now voting for: " + reaction.emoji + " " + name)
    #         poll.votes = poll.votes+1
    #         print(poll.votes)

@bot.command(name='dmcc', help='send dm to camp counsellor')
async def printlist(ctx):
    # userlist.pop(0)
    # userlist.pop(0)
    # userlist.pop(0)
    embed = create_camp_counsellor_msg(userlist)
    for cc in userlist:
        if not cc.bot:
            channel = await cc.create_dm()
            await ctx.send("Your role has been sent %s" %cc.name)

            embed.add_field(name = "Options", value = unicode_letters[0] + " Choose a person to expose their role\n"+unicode_letters[1]+" Find out two roles that are not in the camp\n")
            message = await channel.send(embed=embed)
            await message.add_reaction(unicode_letters[0])
            await message.add_reaction(unicode_letters[1])

            message = await channel.fetch_message(message.id)

            reaction, user = await bot.wait_for('reaction_add', timeout=1.0, check=check)

            reactionTest=get(message.reactions, emoji=unicode_letters[0])
            reactionTest2=get(message.reactions, emoji=unicode_letters[1])
            print(reactionTest.count)
            print(reactionTest2.count)
            print("==================================")
            print(str(message.reactions[0]))
            print(str(message.reactions[1]))
            if(message.reactions[0].count > message.reactions[1].count):
                print(str(message.reactions[0]))
                print(str(message.reactions[1]))
                print("A better")
            elif (message.reactions[0].count < message.reactions[1].count):
                print(str(message.reactions[0]))
                print(str(message.reactions[1].count))
                print("B better")
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
        if wolf.bot:
            continue
        else:
            names.append(wolf.name)
    list_wolves = delimeter.join(names)

    if list_wolves:
        werewolf_str = "Your fellow wolves are:\n" + list_wolves
    else:
        werewolf_str = "Unfortunately, you have no fellow wolves with you... You're on your own!"

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

def create_best_friend_msg(bestie_list):
    names = []
    delimeter = '\n'
    for bestie in bestie_list:
        if bestie.bot:
            continue
        else:
            names.append(bestie.name)
    list_besties = delimeter.join(names)

    if list_besties:
        best_friend_str = "The best friends are:\n" + list_besties
    else:
        best_friend_str = "Unfortunately, your best friend isn't here with you... Try making some friends with the campers!"

    embed = discord.Embed(
        title = "You are a Best Friend!",
        description = "You will have a good time at camp if you get rid of any werewolves and don't accidentally get rid of your best friend - who you know isn't a werewolf.\n\n""" + best_friend_str,
        color = discord.Color.blue()
    )
    embed.set_image(url='https://i.imgur.com/wHgG64a.jpg')
    return embed

def create_wannabe_msg(wolf_list):
    names = []
    delimeter = '\n'
    for wolf in wolf_list:
        if wolf.bot:
            continue
        else:
            names.append(wolf.name)
    list_wolves = delimeter.join(names)

    if list_wolves:
        werewolf_str = "Your fellow wolves are:\n" + list_wolves
    else:
        werewolf_str = "Unfortunately, you have no fellow wolves to cover for... You're on your own!"
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

def create_camp_counsellor_choice(userlist):
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

#################### WIN CONDITIONS LOGIC ###################
async def win_conditions(ctx, eliminated):
    winners = []
    win_roles = []
    for player in eliminated:
        # if introvert is voted, everyone auto loses except introvert
        if player.role == "Introvert":
            win_roles.append("Introvert")
            winners.append(introvert_list[0].name)
            break
        #if werewolf is voted, all campers win
        elif player.role == "Werewolf":
            win_roles.append("Campers")
            for player in camper_list:
                winners.append(player.name)
            break
        #if wannabe voted
        elif player.role == "Wannabe" or player.role == "Camper":
            # If wannabes exist
            if wannabe_list:
                win_roles.append("Wannabe")
                winners.append(wannabe_list[0].name)
            # If werewolves exist
            if werewolf_list:
                win_roles.append("Werewolf")
                for player in werewolf_list:
                    winners.append(player.name)

    embed = discord.Embed(
        title = (f"Winners: {winners}"),
        description = (f"The {win_roles} has/have won! Congratulations!"),
        color = discord.Color.red()
    )
    await ctx.send(embed = embed)
    

bot.run(TOKEN)