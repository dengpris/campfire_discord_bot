# bot.py
from calendar import c
from email.errors import FirstHeaderLineIsContinuationDefect
from tkinter import N

#To resize image:
from PIL import Image
from io import BytesIO

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
from settings_for_roles import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)

#################################
@bot.command(name='timer', help='timer command. usage !timer <num of minutes> <num of seconds>')
async def timer(ctx, minutes, seconds=0):
    moon_dic={0:'', }
    try:
        minuteint = int(minutes)
        secondsint=int(seconds)
        totalseconds=minuteint*60 + secondsint

        totalSecondsLeft=minuteint*60 + secondsint
        if totalseconds > 3600:
            await ctx.send("I dont think im allowed to do go above 60 minutes.")
            raise BaseException
        if totalseconds <= 0:
            await ctx.send("I dont think im allowed to do negatives")
            raise BaseException
        
        moonMessage = await ctx.send("🌑")
        timerMessage = await ctx.send(f"Timer: {minuteint} minutes {secondsint} seconds")
        while True:
            totalSecondsLeft -= 1
            if totalSecondsLeft == 0:

                await timerMessage.edit(content="Ended!")
                break
                #return True

            minuteLeft=totalSecondsLeft//60
            secondsLeft=totalSecondsLeft%60
            if(totalSecondsLeft<totalseconds//5):
                await moonMessage.edit(content=f"🌕")
                await timerMessage.edit(content=f"Timer: {minuteLeft} minutes {secondsLeft} seconds")
            elif(totalSecondsLeft>=totalseconds//5 and totalSecondsLeft<2*totalseconds//5):
                await moonMessage.edit(content=f"🌖")
                await timerMessage.edit(content=f"Timer: {minuteLeft} minutes {secondsLeft} seconds")
            elif(totalSecondsLeft>=2*totalseconds//5 and totalSecondsLeft<3*totalseconds//5):
                await moonMessage.edit(content=f"🌗")
                await timerMessage.edit(content=f"Timer: {minuteLeft} minutes {secondsLeft} seconds")
            elif(totalSecondsLeft>=3*totalseconds//5 and totalSecondsLeft<4*totalseconds//5):
                await moonMessage.edit(content=f"🌘")
                await timerMessage.edit(content=f"Timer: {minuteLeft} minutes {secondsLeft} seconds")
            elif(totalSecondsLeft>=4*totalseconds//5 and totalSecondsLeft<totalseconds):
                await moonMessage.edit(content=f"🌑")
                await timerMessage.edit(content=f"Timer: {minuteLeft} minutes {secondsLeft} seconds")
            
            if (new_day):
                if (total_voted == len(userlist)):
                    await ctx.send("Everybody has voted! Who will be sent home?")
                    return True
                # UPDATE VOTING STATUS EVERY 5 SECONDS
                if secondsLeft%5 == 0: 
                    print(f"poll list:{poll_list}")
                    await ctx.send(embed=create_vote_status_msg(poll_list, secondsLeft))    
                  
            await asyncio.sleep(1)
        await ctx.send(f"{ctx.author.mention} Your countdown Has ended!")
    except ValueError:
        await ctx.send("Must be a number!")

@bot.command(name='werewolfEnd', help='kill the game')
async def werewolfEnd(ctx):
    await ctx.send("imma kill myself")
    exit()

################# SET SETTINGS ####################
def submit_start_settings(number_of_each_role):
    global NUM_OF_EACH_ROLE
    NUM_OF_EACH_ROLE = number_of_each_role.copy()
    global CUSTOM_ROLES
    CUSTOM_ROLES = True

async def show_current_roles(ctx, num_players, custom_roles=False):
    
    #num_players = 3
    roles_listed_out = ""

    if num_players < 3:
        #num_players = 4
        await ctx.send(f"Not enough players... maybe find more friends? {num_players}")
        #await reset_bot(ctx)
    
    if not custom_roles:
        if num_players > 10:
            wolf = int(num_players//2)
            counselor = int(num_players//5)
            wannabe = int(num_players//5)
            campers =  int(num_players//2) - 1
            max_num_roles = {"Werewolf":wolf, "Camp Counselor":counselor, "Wannabe":wannabe, "Introvert":1, "bffpair":1, "Camper":campers}
        else:
            max_num_roles = DEFAULT_ROLE_VALUES[str(num_players)].copy()

        roles_listed_out = "Current Number of Each Role: \n" + "**Werewolves:** " + str(max_num_roles["Werewolf"]) + "\t\n**Camp Counselor:** " + str(max_num_roles["Camp Counselor"]) + "\t\n**Wannabe:** "+ str(max_num_roles["Wannabe"]) + "\t\n**Introvert:** " + str(max_num_roles["Introvert"]) +  "\t\n**Pairs of BFFs:** " + str(max_num_roles["bffpair"]) + "\t\n**Campers:** " + str(max_num_roles["Camper"]) +  "\n\nPlease remember that not all roles may be used during this game session!" 
    else:
        roles_listed_out = "Current Number of Each Role: \n" + "**Werewolves:** " + str(NUM_OF_EACH_ROLE["Werewolf"]) + "\t\n**Camp Counselor:** " + str(NUM_OF_EACH_ROLE["Camp Counselor"]) + "\t\n**Wannabe:** "+ str(NUM_OF_EACH_ROLE["Wannabe"]) + "\t\n**Introvert:** " + str(NUM_OF_EACH_ROLE["Introvert"]) +  "\t\n**Pairs of BFFs:** " + str(NUM_OF_EACH_ROLE["bffpair"]) + "\t\n**Campers:** " + str(NUM_OF_EACH_ROLE["Camper"]) +  "\n\nPlease remember that not all roles may be used during this game session!" 

    embed = create_welcome_camper_msg(roles_listed_out)
    await ctx.send(embed=embed)

    await ctx.send("Do you want to change the number of each role? please enter **y** or **n**")

    def check_y_n(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["y", "n", "!reset"]

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel 

    try:
        msg = await bot.wait_for("message", check=check_y_n, timeout=10.0)
    except asyncio.TimeoutError:
        await reset_bot(ctx)
        return

    if msg.content.lower() == "y":
        await ctx.send("**You said yes!**\n" + settings_usage_text())
        custom_role_numbers = await bot.wait_for("message",check=check)
        while not await correct_settings_input(ctx, num_players, custom_role_numbers.content.split()):
            custom_role_numbers = await bot.wait_for("message",check=check)

        submit_start_settings(set_start_settings(custom_role_numbers.content.split()))
        await see_settings_roles(ctx)
    elif msg.content == "!reset":
        return
    else:
        global CUSTOM_ROLES
        CUSTOM_ROLES = custom_roles

    await ctx.send("Alright! Let the Games BEGIN!!!")

def delete_images(nameList):
    print(f"Deleting images {nameList}")
    for name in nameList:
        print(f"Looking at {name}")
        imagedir = IMAGES_FOLDER + name + ".jpg"
        if os.path.exists(imagedir):
            print("WE FOUND IMAGE ", imagedir)
            os.remove(imagedir)
            print("WE DELETED ", imagedir)
        else:
            print("we couldn't find ", imagedir)
            


################# GAME LOGIC #####################
async def gameLogic(ctx, minutes, seconds, custom_roles=False):
    while(BOT_RUNNING):
        while(GAME_RUNNING):
            print('Game Start!')
            nameList=[member.name for member in userlist]
            print(nameList)
           
            #number of players
            num_players = len(nameList)
            global PARTICIPANT_LIST
            PARTICIPANT_LIST = nameList.copy()

            # save photos of players
            await save_and_resize_avatars(nameList)
            # Show current players
            await send_user_avatar_and_name(ctx, nameList)
          
            # Show current role numbers
            await show_current_roles(ctx, num_players,custom_roles)
            
            # Assign roles to players
            roles_dictionary = NUM_OF_EACH_ROLE
            custom_roles = CUSTOM_ROLES
            game=roles.GameState(nameList, roles_dictionary, True, custom_roles=custom_roles)
            
            # Get unused roles
            global UNUSED_ROLES
            UNUSED_ROLES = game.get_unused_roles()
            get_unused_roles()

            #night time timer
            await asyncio.gather(
                timer(ctx, 0, 30),
                send_role(game, ctx),
            )
            # ensure camp Counselor made choices (if applicalble)   
            global new_day 
            new_day = True

            # SEND VOTING DM TO EACH PLAYER
            # Flow: on_reaction_add 
            global poll_list
            embed = create_poll(userlist, poll_list)
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
            await timer(ctx, 0, 10)#25 before 
            
            # TALLY VOTES
            poll_list.sort(key=lambda x: x.votes, reverse=True)
            
            eliminated = []
            highest_votes = poll_list[0].votes
            print(f"highest votes {highest_votes}")
            for poll in poll_list:     
                if poll.votes == highest_votes:
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
    # SEND DM TO ALL CAMP COUNSELORS
    for cc in camp_counselor_list:
        emoji_idx=0
        if not cc.bot:
            channel = await cc.create_dm()
            embed = await create_camp_counsellor_msg(userlist, channel)
            message = await channel.send(embed=embed)

            for u in userlist:
                await message.add_reaction(unicode_letters[emoji_idx])
                player_emoji_dic[unicode_letters[emoji_idx]]=u.name
                emoji_idx+=1
            
            await message.add_reaction(unicode_letters[emoji_idx])
            await ctx.send("Your role has been sent %s" %cc.name)
    

    ############### CAMP COUNSELLOR SELECTION ################
    def check(reaction, user):
        return user in camp_counselor_list and str(reaction.emoji) in unicode_letters


    campCounsellorsCheckedIn=[]
    camp_counselor_list_names=[cc.name for cc in camp_counselor_list if not cc.bot]
    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
            # if camp counsellor is reacting the first time
            if user.name not in campCounsellorsCheckedIn:
                for letters in unicode_letters: # emoji_idx last + 1 (expose two roles option)
                    if str(reaction.emoji) == str(unicode_letters[emoji_idx]) :
                        #get missing roles
                        task = asyncio.create_task(reveal_two_missing_for_cc(ctx, reaction, user))
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
            break
    return

async def reveal_two_missing_for_cc(ctx, reaction, user):
    def check_missing(reaction, user):
        return user in camp_counselor_list and str(reaction.emoji) in unicode_letters[:3] # A B C
    
    message = await reaction.message.channel.send(embed=choose_two_missing_roles_msg())
    for i in range(3):
        await message.add_reaction(unicode_letters[i])
    
    missing_revealed = set()
    while len(missing_revealed) < 2:
        reaction_two, user_two = await bot.wait_for('reaction_add', timeout = 29.0, check=check_missing)
        embed = discord.Embed()

        await reaction_two.message.channel.send(str(reaction_two.emoji))
        if str(reaction_two.emoji) == unicode_letters[0]: # "A"
            embed = create_cc_missing_reveal_msg(UNUSED_ROLES[0])
            missing_revealed.add(0)
        elif str(reaction_two.emoji) == unicode_letters[1]:
            embed = create_cc_missing_reveal_msg(UNUSED_ROLES[1])
            missing_revealed.add(1)
        else:
            embed = create_cc_missing_reveal_msg(UNUSED_ROLES[2])
            missing_revealed.add(2)
        await reaction_two.message.channel.send(missing_revealed)
        await reaction_two.message.channel.send(embed=embed)
    return
    
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
            if user == message.author:
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
    
    # Delete avatar images
    nameList = PARTICIPANT_LIST.copy()
    delete_images(nameList)
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

    if len(args) !=7 :
        await ctx.send("You need **7** arguments. Please enter 7 numbers, each will correspond to the number of each roles to be used during the game\n"
                        + "Do `$settings <num of total participants> <num of werewolf> <num of Counselor> <num of wannabe> <num of introverts> <num of bffpair> <num of camper>`\n"
                        + "For example: **$settings 3 1 1 0 0 1 3** for 3 participants, 1 werewolf, 1 Counselor, 0 wannabes, 0 introverts, 1 pair of bffs(ie 2 players can have this role), 3 campers. ")
        raise BaseException

    else:
        custom_role_numbers = list(args)
        num_players = int(custom_role_numbers[0])
        custom_role_numbers.pop(0)
        good_input = False
        
        # CHECK IF NUM_PLAYERS IS VALID
        while not good_input:
            if num_players < 3:
                await ctx.send("Need at least 3 players.")
                good_input = False
            else:
                await ctx.send(f"Thank you! You have chosen **{str(num_players)}** players.")
                #await ctx.send(settings_usage_text())
                good_input = True
        
        # Check if the other 6 args are valid. number of players have been saved
        good_input = await correct_settings_input(ctx, num_players, custom_role_numbers)
        if not good_input:
            await ctx.send("We now only need the next **6** arguments. Please send arguments again ex: `1 1 0 0 1 3`")

        while not good_input :
            custom_role_numbers = await bot.wait_for("message",check=check)
            custom_role_numbers = custom_role_numbers.content.split()
            good_input = await correct_settings_input(ctx, num_players, custom_role_numbers)

    submit_start_settings(set_start_settings(custom_role_numbers))
    await see_settings_roles(ctx)


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
    await ctx.send("**ROLES HAVE BEEN RESET TO DEFAULT VALUES**.\n")

################### DM VOTING LOGIC ##################
@bot.event
async def on_reaction_add(reaction, user):
    # make sure this is in DMs
    if not isinstance(reaction.message.channel, discord.DMChannel): return
    # make sure its not bot, make sure reaction is valid and make sure is new day
    if user.bot or new_day==False or str(reaction.emoji) not in unicode_letters: 
        return    
    has_already_voted = False
    voted_name = ""
    # get name associated with emoji
    for poll in poll_list:
        if poll.get_name_from_emoji(reaction.emoji):
            voted_name = poll.user
            break
    for poll in poll_list:    
        if (poll.user == user.name):
            # if player already voted, remove old vote
            if (poll.voted):
                for player in poll_list:
                    if player.user == poll.voted:
                        player.votes -= 1
                        has_already_voted = True
                        break
            poll.voted = voted_name
        
        if (poll.user == voted_name): # the name that was chosen by emoji
            poll.votes = poll.votes+1
            # await user.send("You are now voting for: " + reaction.emoji + " " + voted_name)
            for player in userlist:
                if player.name == poll.user:
                    embed = create_vote_for_msg(player)
                    await user.send(embed=embed)   
    # if voting for the first time, send message to channel
    if not has_already_voted:
        global total_voted
        total_voted += 1


@bot.event
async def on_reaction_remove(reaction, user):
    # make sure this occurs in DMs
    if not isinstance(reaction.message.channel, discord.DMChannel): return
    # make sure its not bot, make sure reaction is valid and make sure is new day
    if user.bot or new_day==False or str(reaction.emoji) not in unicode_letters: 
        return

    unvoted_name = ""
    # get name associated with emoji
    for poll in poll_list:
        if poll.get_name_from_emoji(reaction.emoji):
            unvoted_name = poll.user
            break
    for poll in poll_list:
        if (poll.user == user.name):
            if poll.voted == unvoted_name:
                # await user.send("You are no longer voting for: " + reaction.emoji + " " + unvoted_name)
                poll.voted = ""
                for poll in poll_list:
                    if poll.user == unvoted_name:
                        poll.votes -= 1
                        global total_voted
                        total_voted -= 1
                        break
    # send embed telling player they are no longer voting
    for player in userlist:
        if player.name == unvoted_name:
            embed = create_no_longer_vote_msg(player)
            await user.send(embed=embed)

#################### WIN CONDITIONS LOGIC ###################
async def win_conditions(ctx, eliminated):
    winners = []
    win_roles = []
    global GAME_RUNNING
    if(poll_list[0].votes != 0):
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
            elif player.role == "Wannabe" or player.role == "Camper" or player.role == "Best Friend" or player.role == "Camp Counselor":
                # If wannabes exist
                if wannabe_list:
                    win_roles.append("Wannabe")
                    winners.append(wannabe_list[0].name)
                # If werewolves exist
                if werewolf_list:
                    win_roles.append("Werewolves")
                    for player in werewolf_list:
                        winners.append(player.name)
    else: #No one votes
        #Counts number of total werewolves in game
        total_players = len(player_list)
        if(CUSTOM_ROLES):
            total_werewolf = NUM_OF_EACH_ROLE.get("Werewolf")
        else:
            total_werewolf = DEFAULT_ROLE_VALUES[str(total_players)]["Werewolf"]

        total_unused_werewolf = UNUSED_ROLES.count("Werewolf")

        #If werewolves are all in missing roles
        if(total_werewolf == total_unused_werewolf):
            win_roles.append("Campers")
            for player in camper_list:
                winners.append(player.name)
            for player in camp_counselor_list:
                winners.append(player.name)
            for player in best_friend_list:
                winners.append(player.name)
        #Otherwise, werewolves win
        else:
            win_roles.append("Werewolves")
            for player in werewolf_list:
                winners.append(player.name)
    
    embed = discord.Embed(
        title = ("The {win_roles} has/have won! Congratulations! Winners: "),
        color = discord.Color.red()
    )
    await ctx.send(embed = embed)

    await send_user_avatar_and_name(ctx, winners)

    # Reveal Role
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
# @bot.command(name="show_user", help='shows user avatar')
# async def show_user_avatar(ctx, username):
#     """
#     userlist is a global variable of user types
#     username is the name of user 
#     GOAL: to input a username, and output their photos 
#     - photos should be set to the same size
#     """
#     await ctx.send(userlist)
#     userAvatar = ""
#     avatarjpg = "avatar3.jpg"
#     for member in userlist:
#         if member.name == username:
#             userAvatar = member.avatar_url
#             await ctx.send(userAvatar)
#             await userAvatar.save(avatarjpg)
#             file = discord.File(fp=avatarjpg)

#     await ctx.send("Sending embed")

#     embed = discord.Embed(
#         title = f"This is what {username} looks like!",
#         description = f"Do you like their face?",
#         color = discord.Color.blue()
#     )
#     embed.set_image(url=userAvatar)

#     await ctx.send(embed=embed)

# fcn is only for testing
@bot.command(name="resize_user", help='resize avatar')
async def resize_user(ctx):
    """
    Resize user image, make sure to change avatarjpg and new_avatarjpg
    """

    avatarjpg = "avatar_images/Emiwana.jpg"
    new_avatarjpg = "avatar_images/Emiwana_1.jpg"
    file = discord.File(fp=avatarjpg)
    await ctx.send("Current avatar img", file = file)

    image = Image.open(avatarjpg)
    new_image = image.resize((200, 200)).convert('RGB')
    new_image.save(new_avatarjpg)
    file = discord.File(fp=new_avatarjpg)
    await ctx.send("New avatar img", file = file)

# fcn is only for testing
@bot.command(name = "avatar")
async def avatar(ctx):
 
    # Send user avatar
    await ctx.send(ctx.author.avatar_url)

    # Save avatar url as a file
    avatarjpg = "avatarImages/avatar2.jpg"
    await ctx.author.avatar_url.save(avatarjpg)

    # Send an image file
    file = discord.File(fp=avatarjpg)
    await ctx.send("Enjoy :>", file=file)

    # Send image file IN an embed 
    file = discord.File("werewolf.jpg")
    embed = discord.Embed(
        title = f"This is what a werewolf looks like!",
        description = f"Do you like their face?",
        color = discord.Color.blue()
    )
    embed.set_image(url="attachment://werewolf.jpg")
    await ctx.send(embed=embed,file=file)

    # Send image from folder IN an emebed
    #avatarjpg = "avatar0.jpg"
    file = discord.File(avatarjpg, filename="avatar2.jpg")
    embed = discord.Embed(
        title = f"This is what a werewolf looks like!",
        description = f"Do you like their face?",
        color = discord.Color.blue()
    )
    #attachment://avatar_images/avatar2.jpg
    attachment = "attachment://" + "avatar2.jpg"
    embed.set_image(url=attachment)
    await ctx.send(embed=embed,file=file)
########## ABOVE IS TESTING FCNS ONLY


def resize_image(image_file, width=200, height=200):
    """
    Resizes image to given size

    :image_file:    string of image location (.jpg file)
    :width:         int width (default is 200)
    :height:        int height (default is 200)
    :return:        string location of new image
    """

    #ASSUMING THAT THE . SEPARATES EVERYTHING BEFORE THE .JPG
    #print(f"image_file: {image_file}")
    image_file_split = image_file.split(".")
    #resized_image = image_file_split[0] + "New." + image_file_split[1]
    resized_image = image_file
    print(f"new_image: {resized_image}")

    image = Image.open(image_file)
    new_image = image.resize((width, height)).convert('RGB')
    new_image.save(resized_image)
    return resized_image

async def save_and_resize_avatars(nameList,width=200, height=200):
    """
    Saves avatar images in files: <Name>.jpg
    :namelist:  list of strings of name
    """

    namelist = nameList.copy()
    for member in userlist:
        if len(namelist) != 0:
            if member.name in namelist:
                #Set name for avatar
                avatarjpg = member.name + ".jpg"
                avatardir = IMAGES_FOLDER + avatarjpg
                userAvatar = member.avatar_url
                #Save avatar image
                await userAvatar.save(avatardir)
                #Change avatar image to appropriate size:
                avatardir = resize_image(avatardir,width,height)

async def send_user_avatar_and_name(ctx, nameList, embed_colour=discord.Color.blue(), width=200,height=200):
    """
    :usernames:     string of list of usernames
    :width:         width of avatar to be sent
    :height:        height of avatar to be sent
    """
    usernames = nameList.copy()

    #images_folder = "avatarImages/"
    for member in userlist:
        if len(usernames) != 0:
            if member.name in usernames:
                #Set name for avatar
                avatarjpg = member.name + ".jpg"
                avatardir = IMAGES_FOLDER + avatarjpg
                
                #Change avatar image to appropriate size (assuming that all avatar images are alread 200 by 200):
                if width != 200 and height!=200:
                    avatardir = resize_image(avatardir,width,height)

                #Setup Embed
                file = discord.File(avatardir, filename=avatarjpg)
                embed = discord.Embed(
                    title = member.name,
                    color = embed_colour
                )
                attach_avatar = "attachment://" + avatarjpg
                embed.set_image(url=attach_avatar)
                #Send embed
                await ctx.send(embed=embed,file=file)
                usernames.remove(member.name)


async def reveal_roles(ctx, eliminated, poll_list):
    #sort list from least to greatest
    poll_list.sort(key=lambda x: x.votes, reverse=False)

    text=""
    users_w_same_num_of_votes = []
    voteVal=0
    #iterate through each element in the array, compare each element to voteVal while appending the player name to the text
    #when the element is different to voteVal, update voteVal to the current element value
    # and then print the text value
    for p in poll_list:
        print(p.user+"  "+str(p.votes))
        if p.votes==voteVal:
            text=text+p.user+"\n"
            users_w_same_num_of_votes.append(p.user)
        if p.votes!=voteVal:    
            embed = discord.Embed(
                    title = (f"PEOPLE WITH "+ str(voteVal) +" VOTES"),
                    color = discord.Color.blurple()
                )
            await ctx.send(embed=embed)
            await send_user_avatar_and_name(ctx, users_w_same_num_of_votes, discord.Color.blurple())
            users_w_same_num_of_votes = []
            users_w_same_num_of_votes.append(p.user)
            voteVal=p.votes

    
    embed = discord.Embed(
        title = (f"PEOPLE VOTED OFF WITH {str(voteVal)} VOTES"),
        description = "sORRY but Bye felicIa",
        color = discord.Color.red()
    )

    #print the most voted off person
    await ctx.send(embed=embed)
    await send_user_avatar_and_name(ctx, users_w_same_num_of_votes,discord.Color.red(),400,400)
    #NEED TO DELETE ALL FILES IN ./avatar_images
    return 

bot.run(TOKEN)
