####### GLOBAL VARIABLES #########
unicode_letters = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮"]
userlist=[]
poll_list=[]
player_list=[]
werewolf_list = []
camper_list = []
wannabe_list = []
introvert_list = []
best_friend_list = []
camp_counselor_list = []
total_voted = 0
moonTimerEmojiList=[
                "🌘🌑🌑🌑", 
                "🌗🌑🌑🌑",
                "🌖🌑🌑🌑",
                "🌕🌑🌑🌑",
                "🌕🌘🌑🌑",
                "🌕🌗🌑🌑",
                "🌕🌖🌑🌑",
                "🌕🌕🌑🌑",
                "🌕🌕🌘🌑",
                "🌕🌕🌗🌑",
                "🌕🌕🌖🌑",
                "🌕🌕🌕🌑",
                "🌕🌕🌕🌘",
                "🌕🌕🌕🌗",
                "🌕🌕🌕🌖",
                "🌕🌕🌕🌕"]

########## ROLE IMAGE URLS ###########
welcome_url = 'https://i.imgur.com/OPCZSjx.png'
camper_url = 'https://i.imgur.com/4AYKSl3.jpg'
cc_url = 'https://i.imgur.com/FnS0HP5.jpg'
best_friend_url = 'https://i.imgur.com/wHgG64a.jpg'
werewolf_url = 'https://i.imgur.com/VP45oFp.jpg'
introvert_url = 'https://i.imgur.com/UFh7Xsp.jpg'
wannabe_url = 'https://i.imgur.com/XZSDOEU.jpg'
missing_url = 'https://i.imgur.com/1ADdRCU.jpg'

new_day = False
voting_poll_exists=False

AVATAR_FOLDER = "avatarImages/"
ROLE_FOLDER = "roleImages/"
PARTICIPANT_LIST = []

###############################################

NUM_OF_EACH_ROLE = {"Werewolf":0, "Camp Counselor":0, "Wannabe":0, "Introvert":0, "bffpair":0, "Camper":0}
CUSTOM_ROLES = False

BOT_RUNNING = True
GAME_RUNNING = False

#Default MAXIMUM role values per each number (Note cannot play with 3 players or less)
DEFAULT_ROLE_VALUES = {  "3": {"Werewolf":1, "Camp Counselor":0, "Wannabe":0, "Introvert":0, "bffpair":0, "Camper":2},
                    "4": {"Werewolf":1, "Camp Counselor":1, "Wannabe":1, "Introvert":1, "bffpair":0, "Camper":3}, #7 -> 3
                    "5": {"Werewolf":2, "Camp Counselor":1, "Wannabe":1, "Introvert":1, "bffpair":0, "Camper":3}, #8 -> 3
                    "6": {"Werewolf":2, "Camp Counselor":1, "Wannabe":1, "Introvert":0, "bffpair":1, "Camper":3}, #9 -> 3
                    "7": {"Werewolf":3, "Camp Counselor":1, "Wannabe":0, "Introvert":1, "bffpair":1, "Camper":3}, #10 
                    "8": {"Werewolf":3, "Camp Counselor":2, "Wannabe":1, "Introvert":0, "bffpair":1, "Camper":3}, #11 
                    "9": {"Werewolf":3, "Camp Counselor":1, "Wannabe":2, "Introvert":1, "bffpair":1, "Camper":3}, #12
                    "10": {"Werewolf":4, "Camp Counselor":2, "Wannabe":1, "Introvert":1, "bffpair":1, "Camper":3}} #13
                    
# Default MAXIMUM role values per each number (Note cannot play with 3 players or less)
CUSTOM_ROLE_MAX_LIMIT = {  "3": {"Werewolf":1, "Camp Counselor":6, "Wannabe":2, "Introvert":1, "bffpair":1, "Camper":2},
                            "4": {"Werewolf":2, "Camp Counselor":2, "Wannabe":3, "Introvert":1, "bffpair":1, "Camper":3}, #7 -> 3
                            "5": {"Werewolf":3, "Camp Counselor":3, "Wannabe":4, "Introvert":1, "bffpair":1, "Camper":4}, #8 -> 3
                            "6": {"Werewolf":4, "Camp Counselor":4, "Wannabe":5, "Introvert":1, "bffpair":1, "Camper":5}, #
                            "7": {"Werewolf":5, "Camp Counselor":5, "Wannabe":6, "Introvert":1, "bffpair":1, "Camper":6},
                            "8": {"Werewolf":6, "Camp Counselor":6, "Wannabe":7, "Introvert":1, "bffpair":1, "Camper":7},
                            "9": {"Werewolf":7, "Camp Counselor":7, "Wannabe":8, "Introvert":1, "bffpair":1, "Camper":8},
                            "10": {"Werewolf":8, "Camp Counselor":8, "Wannabe":9, "Introvert":1, "bffpair":1, "Camper":9}}

# Default MINIMUM role values per each number (Note cannot play with 3 players or less)
CUSTOM_ROLE_MIN_LIMIT = {  "3": {"Werewolf":1, "Camp Counselor":0, "Wannabe":0, "Introvert":0, "bffpair":0, "Camper":0},
                            "4": {"Werewolf":1, "Camp Counselor":0, "Wannabe":0, "Introvert":0, "bffpair":0, "Camper":0},
                            "5": {"Werewolf":1, "Camp Counselor":0, "Wannabe":0, "Introvert":0, "bffpair":0, "Camper":0}, 
                            "6": {"Werewolf":1, "Camp Counselor":0, "Wannabe":0, "Introvert":0, "bffpair":0, "Camper":0}, 
                            "7": {"Werewolf":1, "Camp Counselor":0, "Wannabe":0, "Introvert":0, "bffpair":0, "Camper":0},
                            "8": {"Werewolf":1, "Camp Counselor":0, "Wannabe":0, "Introvert":0, "bffpair":0, "Camper":0},
                            "9": {"Werewolf":1, "Camp Counselor":0, "Wannabe":0, "Introvert":0, "bffpair":0, "Camper":0},
                            "10": {"Werewolf":1, "Camp Counselor":0, "Wannabe":0, "Introvert":0, "bffpair":0, "Camper":0}}


ROLE_INFO = {"Werewolf": {"About": "see the other werewolves","Limit": 1, "Required": True},
             "Camper": {"About": "we vibing fham", "Limit": 7, "Required": True},
             "bff_1": {"About": "half of best friends", "Limit": 1, "Required": False},
             "bff_2": {"About": "other half of best friends", "Limit": 1, "Required": False},
             "Camp Counselor": {"About":"does counselling", "Limit": 1, "Required": False},
             "Wannabe": {"About": "does something", "Limit": 1, "Required": False},
             "Introvert": {"About": "we vibing fham 2.0", "Limit": 1, "Required": False}   
    
}

# Default Roles that will always have 3 roles left over
DEFAULT_ROLES = {   "3": {"Werewolf":1, "Camp Counselor":0, "Wannabe":0, "Introvert":0, "bffpair":0, "Camper":2},
                    "4": {"Werewolf":2, "Camp Counselor":1, "Wannabe":0, "Introvert":1, "bffpair":0, "Camper":3}, #7 -> 3
                    "5": {"Werewolf":2, "Camp Counselor":1, "Wannabe":1, "Introvert":1, "bffpair":0, "Camper":3}, #8 -> 3
                    "6": {"Werewolf":2, "Camp Counselor":1, "Wannabe":1, "Introvert":0, "bffpair":1, "Camper":3}, #9 -> 3
                    "7": {"Werewolf":3, "Camp Counselor":1, "Wannabe":0, "Introvert":1, "bffpair":1, "Camper":3}, #10 
                    "8": {"Werewolf":3, "Camp Counselor":2, "Wannabe":1, "Introvert":0, "bffpair":1, "Camper":3}, #11 
                    "9": {"Werewolf":3, "Camp Counselor":1, "Wannabe":2, "Introvert":1, "bffpair":1, "Camper":3}, #12
                    "10": {"Werewolf":4, "Camp Counselor":2, "Wannabe":1, "Introvert":1, "bffpair":1, "Camper":3}} #13

UNUSED_ROLES = []

