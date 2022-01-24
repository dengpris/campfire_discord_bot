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

## CORNER CASE OVER 10 PLAYERS. (CONTAINS ERROR. FIX AS POLISH)
def check_over_ten_players(num_players,role_dict):

    players_roles = []
    for role in role_dict:
        num_of_each_role_available = role_dict[role]
        while num_of_each_role_available != 0:
            players_roles.append(role)
            num_of_each_role_available-=1

    random.shuffle(players_roles)
    
    if num_players < len(players_roles):
        n = len(players_roles) - num_players
        players_roles = players_roles[:len(players_roles)-n]

    # If number of players > number of roles, add access campers
    if num_players > len(players_roles):
        # if role_dict["Camp Counselor"] != 0:
        #     n = num_players - len(players_roles)  
        n = num_players - len(players_roles)  
        while n != 0:
            players_roles.append("Camper")
            n -=1 

    new_role_dict = {"Werewolf":0, "Camp Counselor":0, "Wannabe":0, "Introvert":0, "bffpair":0, "Camper":0}
    for rand_role in players_roles:
        temp_value = new_role_dict[rand_role]
        new_role_dict[rand_role] = temp_value + 1
    
    return new_role_dict

# Settings text
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