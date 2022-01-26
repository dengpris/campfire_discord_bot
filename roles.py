from email.policy import default
import random
import time
from globalvar import *

def increment_round(self):
        self.round += 1

class Player:
    def __init__(self, name, role=None):
        self.name = name
        self.role = role
        
    def get_role_info(self):
        if self.role is not None:
            return self.role
        else: 
            return "You Do not have a role attached to this player"
    
    def set_role(self, Role):
        if self.role is None:
            self.role = Role

    def find_player(self, name):
        if self.name == name:
            return self
        else:
            return None

class GameState:
    def __init__(self, player_names, custom_role_dict, extra_roles=False, custom_roles=False ):
        
        random.seed(time.time())
        self.num_players = len(player_names)
        self.time = "Night"
        print("before nigth")
        self.extra_roles=extra_roles
        
        if custom_roles:
            random_roles, self.unused_roles = self.set_custom_roles(custom_role_dict)
            print("Length of random_roles: ", len(random_roles))
        # Default roles
        else:
            random_roles, self.unused_roles = self.set_default_roles()

        print("after night")
        #Assigning roles
        self.players = [Player(player_names[person], random_roles[person]) for person in range(self.num_players)]

    def get_unused_roles(self):
        return self.unused_roles

    def set_custom_roles(self, custom_role_dict):

        players_roles = []
        unused_roles = []
        
        # If best friends is a role, replace with bff_1 or bff_2
        # Make sure only bestfriends know each other (only pairs know each other)
        if custom_role_dict["bffpair"] != 0:
            num_bff_pairs = custom_role_dict["bffpair"]
            custom_role_dict.pop("bffpair")
            new_bff_roles = {'bff_1': num_bff_pairs, 'bff_2': num_bff_pairs}
            custom_role_dict.update(new_bff_roles)

        # If camp Counselor is one of the roles, make sure theres 3 extra roles.

        for role in custom_role_dict:
                num_of_each_role_available = custom_role_dict[role]
                while num_of_each_role_available != 0:
                    players_roles.append(role)
                    num_of_each_role_available-=1

        random.shuffle(players_roles)

        ### Wouldn't be used with the current logic but save for the future
        ## If number of players < number of roles, remove excess roles
        # if self.num_players < len(players_roles):
        #     n = len(players_roles) - self.num_players
        #     players_roles = players_roles[:len(players_roles)-n]
        ## If number of players > number of roles, add access campers
        # if self.num_players > len(players_roles):
        #     n = self.num_players - len(players_roles)  
        #     while n != 0:
        #         players_roles.append("Camper")
        #         n -=1 
        
        if self.num_players < len(players_roles):
            #if this happens, it should only happen 3 times
            n = len(players_roles) - self.num_players  
            for i in range(n):
                #Always pop index 2
                res = unused_roles.append(players_roles.pop(0))
                
        random.shuffle(players_roles)
        return players_roles, unused_roles

    def set_default_roles(self):
        default_role_dict = {}
        
        # Can't test this tho rip
        if self.num_players > 10 :
            default_role_dict = DEFAULT_ROLES["10"]
            extra_players = self.num_players - 10
            default_role_dict["Camper"] = default_role_dict["Camper"] + extra_players
        else: 
            default_role_dict = DEFAULT_ROLES[str(self.num_players)]

        #picked_roles = default_role_dict.keys()
        players_roles = []
        unused_roles = []

        if default_role_dict["bffpair"] != 0:
            num_bff_pairs = default_role_dict["bffpair"]
            default_role_dict.pop("bffpair")
            new_bff_roles = {'bff_1': num_bff_pairs, 'bff_2': num_bff_pairs}
            default_role_dict.update(new_bff_roles)

        for role in default_role_dict:
            num_of_each_role_available = default_role_dict[role]
            while num_of_each_role_available != 0:
                players_roles.append(role)
                num_of_each_role_available-=1
        
        random.shuffle(players_roles)

        if self.num_players < len(players_roles):
            #if this happens, it should only happen 3 times
            n = len(players_roles) - self.num_players  
            for i in range(n):
                #Always pop index 2
                res = unused_roles.append(players_roles.pop(0))

        random.shuffle(players_roles)
        return players_roles, unused_roles      

    def set_random_roles(self, extra_roles=False):

        roles = {}
        picked_roles=[]
        
        # If we only want required roles (ie werewolf and campers), change the dictiornary to only include those
        if not extra_roles:
            for role in ROLE_INFO:
                if ROLE_INFO[role]["Required"]:
                    roles[role]= ROLE_INFO[role]
        
        #else keep role dictionary
        else: 
            roles = ROLE_INFO.copy()

        players_left = self.num_players
        
        #If more than num of players and we want more roles:
        if self.num_players>5 and extra_roles:
            # Minimum required amount of each role for MORE THAN 5 players
            role_min_limits = {"Werewolf":2, "Camp Counselor":1, "Wannabe":1, "Introvert":1, "bff_1":0, "bff_2":0, "Camper":0}
            picked_roles=role_min_limits.keys()
            
            # Assign roles based on number of players (based on only 5 or 6 or 7=<); remove 5 players to account for the minimum required amount of players
            players_left -= 5

            # If we have => 7 players, 2 of the players will be bffs
            if players_left >= 2:
                role_min_limits['bff_1'] = 1
                role_min_limits['bff_2'] = 1
                # now we have (total players -5 -2 ) players to deal with
                players_left -= (role_min_limits['bff_1'] + role_min_limits['bff_2'])
            
            # If we have 6 players, must have atleast 1 camper
            elif players_left == 1:
                role_min_limits['Camper'] = 1
                # Now we have 0 players to deal with
                players_left -= role_min_limits['Camper']
            
            ###############
            # If we still have players left
            if players_left != 0:
                # Everyone else gets the role of camper
                role_min_limits['Camper'] += players_left
                players_left -= role_min_limits['Camper']

            #players list becomes: ['Camper', 'camper', campler, werewolf, werewolf, introver..... ]
            players = []
            for role in role_min_limits:
                limit = role_min_limits[role]
                while limit != 0:
                    players.append(role)
                    limit -=1

        # Greater than 5 players, but we only want werewolf and camper
        elif self.num_players>5 and not extra_roles:
            role_min_limits = {"Werewolf":2, "Camper":0}
            picked_roles=role_min_limits.keys()
            #NO MATTER HOW MANY PLAYERS ABOVE 5, THERE WILL ONLY EVER BE 2 WEREWOLVES
            players_left -= role_min_limits["Werewolf"]   
            if players_left != 0:
                role_min_limits['Camper'] += players_left
                players_left -= role_min_limits['Camper']

            #players list becomes: ['Camper', 'camper', campler, werewolf, werewolf..]
            players = []
            for role in role_min_limits:
                limit = role_min_limits[role]
                print(limit)
                while limit != 0:
                    players.append(role)
                    limit-=1
        
        else: 
            # if players <=5 then you're only allowed 1 werewolf, everyone else is campers (no additional roles besides werewolf or camper)
            print("less than5")
            role_min_limits = {"Werewolf":1, "Camper":0}
            picked_roles=role_min_limits.keys()
            players_left -= role_min_limits["Werewolf"]   
            if players_left != 0:
                role_min_limits['Camper'] += players_left
                players_left -= role_min_limits['Camper']
            print("test")
            players = []
            for role in role_min_limits:
                limit = role_min_limits[role]
                while limit != 0:
                    print("test")
                    players.append(role)
                    limit-=1
        
        #shuffles order of player roles
        random.shuffle(players)
        #picked roles is just the different roles for the game
        return players, picked_roles
                
    # def tally_votes(self):
    #     votes={}
    #     for player in self.players:
    #         if player.last_voted in votes:
    #             votes[player.last_voted] +=1
    #         else:
    #             votes[player.last_voted] = 1

    #     players_booted = [key  for (key, value) in votes.items() if value == max(votes.values())]        

    #     return players_booted, max(votes.values())
    
    # def check_votes(self):
    #     players_booted, votes = self.tally_votes()
    #     win=False
    #     for player in self.players:
    #         if player.name in players_booted and player.role=="Werewolf":
    #             print(f"You voted the werewolf {player.name} with {votes} votes")
    #             win=True
                
    #     if not win:
    #         print("you did not catch the werewolf. RIP")
            
    #     return win
            

    def set_night(self):
        if self.time == "Day":
            self.time = "Night"
            for player in self.players:
                player.time = "Night"
            return True
        return False
    
    def set_day(self):
        if self.time == "Night":
            self.time = "Day"
            for player in self.players:
                player.time = "Day"
            return True
        return False
    
    def camp_counsellor_looks(self, player_name, chosen_player):
        name_found=False
        for player in self.players:
            if player.name == player_name:
                name_found = True
                if player.role == "Camp Counselor":
                    break
                else:
                    print("you are not a camp counsellor")
                    return False
            if name_found == False:
                print('name not found')
                return False
                
        for player in self.players:
            if player.name == chosen_player:
                print(f'This player is a {player.role}')
                return player.role
        
        print("Chosen player name does not exist")
        return False
                
    # get 2/3 unpicked roles from group
    def camp_counsellor_unpicked(self, player_name):
        # picked_roles = self.picked_roles
        if self.extra_roles == False:
            print("Error, extra roles is false")
            return False
        else:
            name_found=False
            for player in self.players:
                if player.name == player_name:
                    name_found = True
                    if player.role == "Camp Counselor":
                        break
                    else:
                        print("you are not a camp counsellor")
                        return False 
            if name_found == False:
                print("player not found")
                return False
            
            picked_roles = self.picked_roles.copy()
            unpicked_roles = []
            for role in ROLE_INFO.keys():
                if role not in picked_roles:
                    unpicked_roles.append(role)
            random.shuffle(unpicked_roles)
            return unpicked_roles[:2]
                
    #find best friend of 'player_name'
    def best_friend_find_friend(self, player_name):
        player_role = ""
        friend={"bff_1":"bff_2", "bff_2": "bff_1"}
        
        for player in self.players:
            if player.name == player_name:
                if player.role != "bff_1" or player.role != "bff_2":
                    print("you are not one of the bestest friends ever or bffs dont exist this game")
                    return False
                else:
                    player_role = player.role
        if player_role == "":
            print("incorrect player name")
            return False
        
        for player in self.players:
            if player.role == friend[player_role]:
                print(f"your friend is {friend.name}")
                return True
        print("can't find a bff Sadge")
        return False

        
        
            
        


    
    
    



    