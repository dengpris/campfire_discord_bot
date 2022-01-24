# bot.py
from calendar import c
from email.errors import FirstHeaderLineIsContinuationDefect
from tkinter import N

from numpy import maximum
import os
from pickle import FALSE
import random
import asyncio
from tabnanny import check
from webbrowser import Elinks
import roles
import sys

from discord.ext import commands
from dotenv import load_dotenv
from discord.utils import get

from poll import *
from embeds import *
from globalvar import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)

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
                #return True
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
def settings_usage_text():
    return "You need **6** arguments. Please enter 6 numbers, each will correspond to the number of each roles to be used during the game\n" + "Do `<num of werewolf> <num of Counselor> <num of wannabe> <num of introverts> <num of bffpair> <num of camper>`\n" + "For example: **1 1 0 0 1 3** for 1 werewolf, 1 Counselor, 0 wannabes, 0 introverts, 1 pair of bffs(ie 2 players can have this role), 3 campers."

def set_start_settings(custom_role_numbers):
    list_of_roles = ["Werewolf", "Camp Counselor", "Wannabe", "Introvert", "bffpair","Camper"]
    number_of_each_role =  {"Werewolf":0, "Camp Counselor":0, "Wannabe":0, "Introvert":0, "bffpair":0, "Camper":0}
    print(f"CUSTOM ROLE NUMBERS IS {custom_role_numbers}")
    for i in range(6):
            role_int = int(custom_role_numbers[i])
            number_of_each_role[list_of_roles[i]] = role_int
    global NUM_OF_EACH_ROLE
    NUM_OF_EACH_ROLE = number_of_each_role.copy()
    global CUSTOM_ROLES
    CUSTOM_ROLES = True

# Assume list_of_roles are all valid numbers
def turn_strList_to_intList(strList):
    intList = []
    for str in strList:
        intList.append(int(str))
    return intList

def valid_role_settings(num_players, custom_role_numbers):
    
    custom_role_numbers = turn_strList_to_intList(custom_role_numbers)
    minimum_limit = []
    maximum_limit = []
    role_names = ["Werewolf", "Camp Counselor", "Wannabe", "Introvert", "bffpair","Camper"]
    error_line = ""
    role_count = 0

    #if more than 10 players, return a different set of max
    if num_players > 10:
        # ["Werewolf", "Camp Counselor", "Wannabe", "Introvert", "bffpair","Camper"]
        minimum_limit = [1, 0, 0, 0, 0, 0]
        maximum_limit = [num_players-2, num_players-2, num_players-1, 1, 1, num_players-1]
    else:
    # Note that these global variables also follow same logic as above, but it will give you the opportunity to edit each one.
        minimum_limit = list(CUSTOM_ROLE_MIN_LIMIT[str(num_players)].values())
        maximum_limit = list(CUSTOM_ROLE_MAX_LIMIT[str(num_players)].values())

    for i in range(6):
        
        if minimum_limit[i] > custom_role_numbers[i]:
            error_line += "**ERROR!** The " + role_names[i] + " amount: **" + str(custom_role_numbers[i]) + "** does not meet the __MINIMUM__ requirement of **" + str(minimum_limit[i]) + "** " + role_names[i] + "\n"
        if maximum_limit[i] < custom_role_numbers[i]:
            error_line += "**ERROR!** The " + role_names[i] + " amount: **" + str(custom_role_numbers[i]) + "** does not meet the __MAXIMUM__ requirement of **" + str(minimum_limit[i]) + "** " + role_names[i] + "\n"
        if role_names[i] == "bffpair":
            role_count += custom_role_numbers[i]*2
        else:
            role_count += custom_role_numbers[i]

    #Check if they sellected atleast 1 Camp Counselor
    if custom_role_numbers[1] != 0:
        #If 1 Camp Counselor is selected, make sure we have an extra 3 roles
        required_role_count = num_players+3
        if role_count != required_role_count:
            error_line += "**ERROR!** Currently, you chose **" + str(role_count) + "** roles. We require __exactly__ **" + str(required_role_count) + "** because you want a __Camp Counselor__ (Note: Pair of BFFs counts as 2 roles)\n"
    else:
        required_role_count = num_players
        if role_count != required_role_count:
            error_line += "**ERROR!** Currently, you chose **" + str(role_count) + "** roles. We require __exactly__ **" + str(required_role_count) + "** (Note: Pair of BFFs counts as 2 roles)\n"
    
    if error_line != "":
        return False, error_line
    else:
        return True, error_line

async def send_Error(ctx, error):
    error_dict = {"1": ("**ERROR!** "+ settings_usage_text()), "2": "**ERROR!** Must be numbers only!"}

    try:
        int(error)
    except(ValueError):
        error_line = error
    else:
        if int(error) >2 or int(error) < 0:
            error_line = "**ERROR!** Unknown Error"
        else:
            error_line = error_dict[str(error)]

    await ctx.send(error_line)

def all_numbers(settings_input_list):
    for i in range(6):
            try:
                int(settings_input_list[i])
            except ValueError:
                return False
    return True

async def correct_settings_input(ctx, num_players, settings_input):
    settings_input_list = settings_input.content.split()
    num_args = len(settings_input_list)
    if num_args != 6:
        await send_Error(ctx, 1)
        return False
    elif not all_numbers(settings_input_list):
        await send_Error(ctx, 2)
        return False
    else:
        valid_settings, error_msg =valid_role_settings(num_players,settings_input_list)
        if not valid_settings:
            await send_Error(ctx, error_msg)
            return False
    return True

async def show_current_roles(ctx, num_players, custom_roles=False):
    
    num_players = 3
    if num_players < 3:
        await ctx.send("Not enough players... maybe find more friends?")
        #exit()
    
    if not custom_roles:
        if num_players > 10:
            num_players = 10
        
        max_num_roles = DEFAULT_ROLE_VALUES[str(num_players)] 
        role_list = "Current Number of Each Role: \n" + "**Werewolves:** " + str(max_num_roles["Werewolf"]) + "\t\n**Camp Counselor:** " + str(max_num_roles["Camp Counselor"]) + "\t\n**Wannabe:** "+ str(max_num_roles["Wannabe"]) + "\t\n**Introvert:** " + str(max_num_roles["Introvert"]) +  "\t\n**Pairs of BFFs:** " + str(max_num_roles["bffpair"]) + "\t\n**Campers:** " + str(max_num_roles["Camper"]) +  "\n\nPlease remember that not all roles may be used during this game session!" 
    
        embed = create_welcome_camper_msg(role_list)
        await ctx.send(embed=embed)

    await ctx.send("Do you want to change the number of each role? please enter **y** or **n**")

    def check_y_n(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and \
        msg.content.lower() in ["y", "n"]

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel 

    msg = await bot.wait_for("message", check=check_y_n)
    if msg.content.lower() == "y":
        await ctx.send("**You said yes!**\n" + settings_usage_text())
        custom_role_numbers = await bot.wait_for("message",check=check)

        while not await correct_settings_input(ctx, num_players, custom_role_numbers):
            custom_role_numbers = await bot.wait_for("message",check=check)

        set_start_settings(custom_role_numbers.content.split())
        await see_settings_roles(ctx)

    else:
        global CUSTOM_ROLES
        CUSTOM_ROLES = False

    await ctx.send("Alright! Let the Games BEGIN!!!")

################# GAME LOGIC #####################
async def gameLogic(ctx, minutes, seconds, custom_roles=False):
    while(BOT_RUNNING):
        while(GAME_RUNNING):
            print('Game Start!')
            nameList=[member.name for member in userlist]
            print(nameList)

            #number of players
            num_players = len(nameList)
            await show_current_roles(ctx, num_players,custom_roles)

            roles_dictionary = NUM_OF_EACH_ROLE
            custom_roles = CUSTOM_ROLES
            game=roles.GameState(nameList, roles_dictionary, True, custom_roles=custom_roles)
            # game.set_random_roles()
            global UNUSED_ROLES
            UNUSED_ROLES = game.get_unused_roles()
            get_unused_roles()

            await send_role(game,ctx)
            print(game.players)
            print("printing game object")
            print(game)
            #night time timer
            await timer(ctx, 0, 5)
            await ctx.send("Werewolf list")
            await ctx.send(werewolf_list)
            # ensure camp Counselor made choices (if applicalble)

            embed = create_poll(userlist, poll_list)
            #member = ctx.message.author
            for user in userlist:
                if user.bot == False: # do not send messages to yourself
                    channel = await user.create_dm()
                    message = await channel.send(embed=embed)

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

            await reveal_roles(ctx, eliminated, poll_list)
            await win_conditions(ctx, eliminated)

            

    #timer ends, initialze vote
    #player_booted, num_votes = game.tally_votes()

        #determine winners

def get_unused_roles():
    unused_roles = UNUSED_ROLES.copy()
    print(f"UNUSED_ROLES ARE: {unused_roles}")
    return unused_roles

################ ROLE HANDOUT TO DMS ######################
async def send_role(game,ctx):
    for player in game.players:
        player_list.append(roles.Player(player.name, player.get_role_info()))
        print(player.name + " "+ player.get_role_info())
        if player.get_role_info() == "Werewolf": 
            for user in userlist:
                if user.name == player.name:
                    werewolf_list.append(user)
            await ctx.send(werewolf_list)
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
        elif  (player.get_role_info() == "Camp Counselor"): #camp_counselor
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
        embed = create_werewolf_msg(werewolf_list, werewolf)
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
        embed = create_best_friend_msg(best_friend_list, best_friend)
        if not best_friend.bot:
            channel = await best_friend.create_dm()
            msg = await channel.send(embed=embed)
            await ctx.send("Your role has been sent %s!" %best_friend.name)

    player_emoji_dic={}
    for cc in camp_counselor_list:
        emoji_idx=0
        if not cc.bot:
            channel = await cc.create_dm()
            embed = await create_camp_counsellor_msg(userlist, channel)
            message = await channel.send(embed=embed)

            for u in userlist:
                if not u.bot:
                    await message.add_reaction(unicode_letters[emoji_idx])
                    player_emoji_dic[unicode_letters[emoji_idx]]=u.name
                    emoji_idx+=1
            
            await message.add_reaction(unicode_letters[emoji_idx])
            await ctx.send("Your role has been sent %s" %cc.name)
    

    ############### CAMP COUNSELLOR SELECTION ################
    def check(reaction, user):
        return user in userlist and str(reaction.emoji) in unicode_letters

    campCounsellorsCheckedIn=[]
    camp_counselor_list_names=[cc.name for cc in camp_counselor_list if not cc.bot]
    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=15.0, check=check)
            # if camp counsellor is reacting the first time
            if user.name not in campCounsellorsCheckedIn:
                for letters in unicode_letters:
                    if str(reaction.emoji) == str(unicode_letters[emoji_idx]) :
                        #get missing roles
                        await reaction.message.channel.send("These roles are missing")
                        # UNCOMMENT THIS WHEN MISSING ROLES LOGIC STARTS WORKING
                        # embed = create_cc_missing_reveal_msg(role_one)
                        # await reaction.message.channel.send(embed=embed)
                        # embed = create_cc_missing_reveal_msg(role_two)
                        # await reaction.message.channel.send(embed=embed)
                        campCounsellorsCheckedIn.append(user.name)
                        break
                    
                    elif str(reaction.emoji) == str(letters):
                        r=""
                        for p in game.players:
                            if p.name==player_emoji_dic[str(reaction.emoji)]:
                                r=p.role
                        
                        for p in userlist:
                            if p.name==player_emoji_dic[str(reaction.emoji)]:
                                embed = create_cc_role_reveal_msg(p, r)
                                await reaction.message.channel.send(embed=embed)
                        campCounsellorsCheckedIn.append(user.name)
                        break
            
            if all(elem in campCounsellorsCheckedIn for elem in camp_counselor_list_names):
                break
        except asyncio.TimeoutError:
            print("break heare istg")
            break
            
################ START GAME ######################
@bot.command(name='start', help='start the game')
async def start(ctx):
    global GAME_RUNNING
    if(GAME_RUNNING == False):
        GAME_RUNNING = True
        # Send message React to Join Game then adds a check emoji
        message = await ctx.send("React to join game!")
        await message.add_reaction('✅')

        # Waits 5 seconds for people to react
        moon_message = await ctx.send(5 * "🌕")
        for i in range(4,0,-1):
            await asyncio.sleep(1)
            update_moon = i * "🌕"
            await moon_message.edit(content=update_moon)
        await moon_message.delete()
        await ctx.send("\n**Time is up!**\nHere's everyone that made it to camp:")

        message = await ctx.channel.fetch_message(message.id)
        reaction = message.reactions[0] # checkmark reactions only
        
        async for user in reaction.users():
            if user.bot:
                continue
            else:
                userlist.append(user)
                await ctx.send(user.name) 
        await gameLogic(ctx, 1, 1, CUSTOM_ROLES)
    else:
        await ctx.send("The game is running already! Type !reset if you want to restart the game.")

@bot.command(name="reset", help='reset bot')
async def reset_bot(ctx):
    global GAME_RUNNING
    userlist.clear()
    poll_list.clear()
    player_list.clear()
    werewolf_list.clear()
    camper_list.clear()
    wannabe_list.clear()
    introvert_list.clear()
    best_friend_list.clear()
    camp_counselor_list.clear()

    GAME_RUNNING = False
    await ctx.send("Resetting!")

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
    NUM_OF_EACH_ROLE = number_of_each_role.copy()
    global CUSTOM_ROLES
    CUSTOM_ROLES = True

@bot.command(name="see_roles", help='see current custom role number settings (note that default will set all to 0)')
async def see_settings_roles(ctx):
    await ctx.send("Current Customized Number of Each Role: \n" + 
                    "**Werewolves:** " + str(NUM_OF_EACH_ROLE["Werewolf"]) + "\t**CampCounsellor:** " + str(NUM_OF_EACH_ROLE["Camp Counselor"]) +
                    "\t**Wannabe:** "+ str(NUM_OF_EACH_ROLE["Wannabe"]) + "\t**Introvert:** " + str(NUM_OF_EACH_ROLE["Introvert"]) + 
                    "\t**Pairs of BFFs:** " + str(NUM_OF_EACH_ROLE["bffpair"]) + "\t**Campers:** " + str(NUM_OF_EACH_ROLE["Camper"]))

@bot.command(name="reset_roles", help='reset the roles to have default values')
async def reset_roles(ctx):
    global CUSTOM_ROLES
    CUSTOM_ROLES = False
    global NUM_OF_EACH_ROLE
    NUM_OF_EACH_ROLE = {"Werewolf":0, "Camp Counselor":0, "Wannabe":0, "Introvert":0, "bffpair":0, "Camper":0}
    ## Wrong information
    await ctx.send("**ROLES HAVE BEEN RESET TO DEFAULT VALUES**.\n" +
                    "**If less than or equal to 5 players:**\t1 werewolf, 4 or less campers.\n" + 
                    "**If 6 players:**\t2 werewolf, 1 wannabe, 1 introvert, 1 camp Counselor, 1 camper\n" + 
                    "**If 7 or more players:**\t2 werewolf, 1 wannabe, 1 introvert, 1 camp Counselor, 2 or more campers")


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

#################### WIN CONDITIONS LOGIC ###################
async def win_conditions(ctx, eliminated):
    winners = []
    win_roles = []
    global GAME_RUNNING
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
            for player in camp_counselor_list:
                winners.append(player.name)
            for player in best_friend_list:
                winners.append(player.name)
            break
        #if wannabe or camper voted
        elif player.role == "Wannabe" or player.role == "Camper" or player.role == "Best Friend" or player.role == "Camp Counsellor":
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

    text=""
    for u in player_list:
        text=text+u.name+" is a "+u.role+"\n"

    embed = discord.Embed(
        title = ("All Roles Revealed:"),
        description = (text),
        color = discord.Color.blurple()
    )
    await ctx.send(embed = embed)
    GAME_RUNNING=False

###################### REVEAL LOGIC ######################
async def reveal_roles(ctx, eliminated, poll_list):
    poll_list.sort(key=lambda x: x.votes, reverse=False)

    text=""
    voteVal=0
    for p in poll_list:
        print(p.user+"  "+str(p.votes))
        if p.votes==voteVal:
            text=text+p.user+"\n"
        if p.votes!=voteVal:    
            embed = discord.Embed(
                    title = (f"People with "+ str(voteVal) +" votes"),
                    description = (text),
                    color = discord.Color.blurple()
                )
            await ctx.send(embed=embed)

            text=""
            text=text+p.user+"\n"
            voteVal=p.votes
    embed = discord.Embed(
        title = (f"People voted off"),
        description = (text),
        color = discord.Color.red()
    )
    await ctx.send(embed=embed)
    
# (ppl who weren't voted off)
# (ppl who were voted off AND their roles) 
# (which and how many camper roles that were used) 
# (which and how many werewolves/wannabe roles that were used) 
# (missing roles)
# (who won campers or werewolves)
    return 
bot.run(TOKEN)