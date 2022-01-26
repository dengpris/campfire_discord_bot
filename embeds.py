# embeds.py
import discord
from globalvar import *

# all functions to create embeds go here
def create_welcome_camper_msg(role_list):
    embed = discord.Embed(
        title = "Welcome to the CAMP!",
        description = "These are the list of roles!\n\n **Note:** Not all roles may be used during this game session!\n\n" + role_list,
        color = discord.Color.blue()
    )
    embed.set_image(url=welcome_url)
    return embed

async def create_camp_counsellor_msg(userlist, channel):
                
    embed = discord.Embed(
        title = "You are a Camp Counsellor!",
        description = "You will have a good trip if you get rid of any werewolves and don't accidentally get rid of camper. Luckily, you have extra privileges and can figure out who one camper is or who two of the missing ones were.\n\n",
        color = discord.Color.blue()
    )

    emoji_idx=0
    value = ""
    for u in userlist:
        name = u.name
        emoji = unicode_letters[emoji_idx]
        value = value + emoji + " " + name + "\n" 
        # update global variable poll_list, which maps emojis to names
        # choice_list.append(poll(name, emoji))
        emoji_idx+=1
    value = value + unicode_letters[emoji_idx] + " Expose two roles not in the game\n"
    embed.add_field(name = "Options", value = value)

    # embed.add_field(name = "Options", value = unicode_letters[0] + " Choose a person to expose their role\n"+unicode_letters[1]+" Find out two roles that are not in the camp\n")
    embed.set_image(url=cc_url)
    return embed

def create_camper_msg():
    embed = discord.Embed(
        title = "You are a Camper!",
        description = "You will have a great time at camp if you get rid of any werewolves and don't accidentally kick out a fellow camper. You just want to have fun at camp.",
        color = discord.Color.blue()
    )
    embed.set_image(url=camper_url)
    return embed

def create_werewolf_msg(wolf_list, me):
    names = []
    delimeter = '\n'
    for wolf in wolf_list:
        if wolf.bot or wolf == me:
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
    embed.set_image(url=werewolf_url)
    return embed

def create_introvert_msg():
    embed = discord.Embed(
        title = "You are an Introvert!",
        description = "You do not like camp, but your mom made you come. You have to figure out a way to go home without her blaming you. You will have a good trip if you get kicked out in the morning.",
        color = discord.Color.gold()
    )
    embed.set_image(url=introvert_url)
    return embed

def create_best_friend_msg(bestie_list, me):
    names = []
    delimeter = '\n'
    for bestie in bestie_list:
        if bestie.bot or bestie == me:
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
    embed.set_image(url=best_friend_url)
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
    embed.set_image(url=wannabe_url)
    return embed

############ EMBEDS FOR CAMP COUNSELLOR REVEAL ##############
def create_cc_role_reveal_msg(user, role):
    color = discord.Color.blurple()
    description = ""
    # camper team is blue
    if role == "Camper" or role == "Best Friend" or role == "Camp Counselor" or role == "Camp Counsellor":
        color = discord.Color.blue()
        description = "This player is a fellow teammate! Make sure they aren't voted off!"
    # werewolf team is red
    if role == "Werewolf":
        color = discord.Color.dark_red()
        description = "Uh oh! This player is a werewolf! Make sure they are voted off in the morning!"
    if role == "Wannabe":
        color = discord.Color.dark_orange()
        description = "This person wants to be friends with the werewolves and will protect them at all costs. Don't let them fool you!"
    # introvert yellow
    if role == "Introvert":
        color = discord.Color.gold()
        description = "This player is an introvert and will try to go home no matter what! Do not send them home!"

    embed = discord.Embed(
        title = f"{user.name} is a {role}!",
        description = f"{description}",
        color = color
    )
    embed.set_image(url=user.avatar_url)
    return embed

def choose_two_missing_roles_msg():
    embed = discord.Embed(
        title = "Three people have gone missing!",
        description = "The missing people trouble you greatly, so you decide to look into this a bit further. You may choose to expose two of the three missing roles.",
        color = discord.Color.blurple()
    )
    embed.set_image(url=missing_url)
    return embed

def create_cc_missing_reveal_msg(role):
    color = discord.Color.blurple()
    url = ""
    # camper team is blue
    if role == "Camper":
        color = discord.Color.blue()
        url = camper_url
    elif role == "Best Friend":
        color == discord.Color.blue()
        url = best_friend_url
    elif role == "Camp Counselor" or role == "Camp Counsellor":
        color = discord.Color.blue()
        url = cc_url
    # werewolf team is red
    elif role == "Werewolf":
        color = discord.Color.dark_red()
        url = werewolf_url
    elif role == "Wannabe":
        color = discord.Color.dark_orange()
        url = wannabe_url
    # introvert yellow
    elif role == "Introvert":
        color = discord.Color.gold()
        url = introvert_url
    
    embed = discord.Embed(
        title = f"A {role} is missing!",
        description = f"One of the missing roles is a {role}.",
        color = color
    )
    embed.set_image(url=url)
    return embed

############## VOTE FOR MESSAGE EMBED #################
def create_vote_for_msg(user):
    embed = discord.Embed(
        title = f"You will vote for {user.name}",
        color = discord.Color.green()
    )
    embed.set_image(url=user.avatar_url)
    return embed

def create_no_longer_vote_msg(user):
    embed = discord.Embed(
        title = f"You are no longer voting for {user.name}",
        color = discord.Color.dark_red()
    )
    embed.set_image(url=user.avatar_url)
    return embed

def create_vote_status_msg(poll_list, seconds):
    name_list = ""
    voted_emoji = ""
    
    for player in poll_list:
        name_list = name_list + "\n" + player.user
        if player.voted:
            voted_emoji = voted_emoji + "\n" + "✅"
        else:
            voted_emoji = voted_emoji + "\n" + "❌"
    
    embed = discord.Embed(
        title = f"There are {seconds} seconds left to vote...")
    
    embed.add_field(name= "Player", value= name_list, inline= True)
    embed.add_field(name= "Voted", value= voted_emoji, inline= True)
        
    return embed