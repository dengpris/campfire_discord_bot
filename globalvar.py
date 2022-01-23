####### GLOBAL VARIABLES #########
unicode_letters = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮"]
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

NUM_OF_EACH_ROLE = {"Werewolf":0, "Camp Counselor":0, "Wannabe":0, "Introvert":0, "bffpair":0, "Camper":0}
CUSTOM_ROLES = False

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
DEFAULT_ROLE_MAX_LIMIT = {  "3": {"Werewolf":1, "Camp Counselor":0, "Wannabe":1, "Introvert":1, "bffpair":0, "Camper":2},
                            "4": {"Werewolf":1, "Camp Counselor":1, "Wannabe":1, "Introvert":1, "bffpair":0, "Camper":3}, #7 -> 3
                            "5": {"Werewolf":2, "Camp Counselor":1, "Wannabe":1, "Introvert":1, "bffpair":0, "Camper":3}, #8 -> 3
                            "6": {"Werewolf":2, "Camp Counselor":2, "Wannabe":1, "Introvert":1, "bffpair":1, "Camper":4}, #
                            "7": {"Werewolf":3, "Camp Counselor":2, "Wannabe":2, "Introvert":1, "bffpair":1, "Camper":5},
                            "8": {"Werewolf":3, "Camp Counselor":2, "Wannabe":2, "Introvert":1, "bffpair":1, "Camper":5},
                            "9": {"Werewolf":4, "Camp Counselor":2, "Wannabe":2, "Introvert":1, "bffpair":1, "Camper":6},
                            "10": {"Werewolf":4, "Camp Counselor":2, "Wannabe":2, "Introvert":1, "bffpair":1, "Camper":7}}

# Default MAXIMUM role values per each number (Note cannot play with 3 players or less)
DEFAULT_ROLE_MIN_LIMIT = {  "3": {"Werewolf":1, "Camp Counselor":0, "Wannabe":1, "Introvert":1, "bffpair":0, "Camper":2},
                            "4": {"Werewolf":1, "Camp Counselor":1, "Wannabe":1, "Introvert":1, "bffpair":0, "Camper":3}, #7 -> 3
                            "5": {"Werewolf":2, "Camp Counselor":1, "Wannabe":1, "Introvert":1, "bffpair":0, "Camper":3}, #8 -> 3
                            "6": {"Werewolf":2, "Camp Counselor":2, "Wannabe":1, "Introvert":1, "bffpair":1, "Camper":4}, #
                            "7": {"Werewolf":3, "Camp Counselor":2, "Wannabe":2, "Introvert":1, "bffpair":1, "Camper":5},
                            "8": {"Werewolf":3, "Camp Counselor":2, "Wannabe":2, "Introvert":1, "bffpair":1, "Camper":5},
                            "9": {"Werewolf":4, "Camp Counselor":2, "Wannabe":2, "Introvert":1, "bffpair":1, "Camper":6},
                            "10": {"Werewolf":4, "Camp Counselor":2, "Wannabe":2, "Introvert":1, "bffpair":1, "Camper":7}}