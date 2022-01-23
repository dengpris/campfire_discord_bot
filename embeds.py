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
    embed.set_image(url='https://i.imgur.com/OPCZSjx.png')
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
        if not u.bot:
            name = u.name
            emoji = unicode_letters[emoji_idx]
            value = value + emoji + " " + name + "\n" 
            # update global variable poll_list, which maps emojis to names
            # choice_list.append(poll(name, emoji))
            emoji_idx+=1
    value = value + unicode_letters[emoji_idx] + " Expose two roles not in the game\n"
    embed.add_field(name = "Options", value = value)

    # embed.add_field(name = "Options", value = unicode_letters[0] + " Choose a person to expose their role\n"+unicode_letters[1]+" Find out two roles that are not in the camp\n")
    embed.set_image(url='https://i.imgur.com/FnS0HP5.jpg')

    return embed

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

def create_best_friend_msg(bestie_list, me):
    names = []
    delimeter = '\n'
    for bestie in bestie_list:
        if bestie.bot or bestie==me:
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