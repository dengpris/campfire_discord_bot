from discord.utils import get
from globalvar import *


## CORNER CASE OVER 10 PLAYERS. (CONTAINS ERROR. FIX AS POLISH)
def check_over_ten_players(num_players,role_dict):
    """
    Check if the combination of roles is playable for over 10 players
    [Note]: Not working

    :num_players:   Number of player participants
    :role_dict:     Dictionary where keys are the role names and values are the number of instances of said role
    """
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

#Edit be a global var
def settings_usage_text():
    """
    Returns the instructions to change the role settings
    """
    return "You need **6** arguments. Please enter 6 numbers, each will correspond to the number of each roles to be used during the game\n" + "Do `<num of werewolf> <num of Counselor> <num of wannabe> <num of introverts> <num of bffpair> <num of camper>`\n" + "For example: **1 1 0 0 1 3** for 1 werewolf, 1 Counselor, 0 wannabes, 0 introverts, 1 pair of bffs(ie 2 players can have this role), 3 campers."

def set_start_settings(custom_role_numbers):
    """
    Organizes the given numbers for each role into a dictionary where the role is the key and the number of each role is the value.

    :custom_role_numbers:           A list of strings that have the number(as a string) of each role in order of {Werewolf, Camp Counselor, Wannabe, Introvert, PairofBFFs, Campers}
    :return (number_of_each_role):  A dictionary specifying the number of each role and the role it's related to
    """

    #Edit be a globalvar
    list_of_roles = ["Werewolf", "Camp Counselor", "Wannabe", "Introvert", "bffpair","Camper"]
    number_of_each_role =  {"Werewolf":0, "Camp Counselor":0, "Wannabe":0, "Introvert":0, "bffpair":0, "Camper":0}
    for i in range(6):
            role_int = int(custom_role_numbers[i])
            number_of_each_role[list_of_roles[i]] = role_int
    return number_of_each_role

# Assume list_of_roles are all valid numbers
def turn_strList_to_intList(strList):
    """
    Turns a list of strings into a list of integers

    :strList:             a list of strings
    :return (intList):    a list of integers
    """
    intList = []
    for str in strList:
        intList.append(int(str))
    return intList

def valid_role_settings(num_players, custom_role_numbers):
    """
    Checks to see if role combination is playable depending on the number of player participants
    Takes global values to limit role numbers for num_players 3-10
    If more than 10 players, uses a set equation to calculate limit role numbers
    Checks to see if current role numbers are within the max and min limits
    Checks to see if there are enough roles for all players

    :num_players:           number of player participants
    :custom_role_numbers:   a list of strings that have the number(as a string) of each role in order of {Werewolf, Camp Counselor, Wannabe, Introvert, PairofBFFs, Campers}
    :return_1:              True if all coniditons are met else False
    :return_2 (error_line): Any error messages
    """
    #Edit change into a list of ints before input
    custom_role_numbers = turn_strList_to_intList(custom_role_numbers)
    minimum_limit = []
    maximum_limit = []
    #Edit be a global Var
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
            error_line += "**ERROR!** The " + role_names[i] + " amount: **" + str(custom_role_numbers[i]) + "** does not meet the __MAXIMUM__ requirement of **" + str(maximum_limit[i]) + "** " + role_names[i] + "\n"
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
    """
    Sends an error message to discord 

    :ctx:       passed in to write messages to discord
    :error:     integer or a string. If it's an interger, error message is taken from error_dict. If its a string, the error message is the string
    """

    #COULD BE IN GLOBAL VAR
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
    """
    Checks if a list of strings can be converted to a list of integers 

    :settings_input_list:   a list of strings
    :return:    True if the above statement is True, else returns false
    """
    for i in range(len(settings_input_list)):
            try:
                int(settings_input_list[i])
            except ValueError:
                return False
    return True

async def correct_settings_input(ctx, num_players, settings_input):
    """
    Checks if role_settings input is valid. This will check for:
    - number of arguments == 6 (the number of different roles we currently have)
    - all arguments in the list is a number
    - the combined roles provide proper playability (see valid_role_settings fcn)
    
    :ctx:            passed in to write messages to discord
    :num_players:    number of player participants
    :settings_input: a list of strings that have the number(as a string) of each role in order of {Werewolf, Camp Counselor, Wannabe, Introvert, PairofBFFs, Campers}
    :return:         Returns False and if not all conditions are met, else returns True
    """
    #settings_input_list = settings_input.content.split()
    settings_input_list = settings_input.copy()
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


