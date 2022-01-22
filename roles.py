import random

ROLE_INFO = {"Werewolf": {"About": "see the other werewolves","Limit": 1, "Required": True},
             "Camper": {"About": "we vibing fham", "Limit": 7, "Required": True},
             "bff_1": {"About": "half of best friends", "Limit": 1, "Required": False},
             "bff_2": {"About": "other half of best friends", "Limit": 1, "Required": False},
             "Camp Counselor": {"About":"does counselling", "Limit": 1, "Required": False},
             "Wannabe": {"About": "does something", "Limit": 1, "Required": False},
             "Introvert": {"About": "we vibing fham 2.0", "Limit": 1, "Required": False}   
    
}


def increment_round(self):
        self.round += 1

class Player:
    def __init__(self,name, role=None):
        self.name = name
        self.role = ROLE_INFO[role]
        self.round = 0
        
    def get_role_info(self):
        if self.role is not None:
            return ROLE_INFO[self.role]["About"]
        else: 
            return "You Do not have a role attached to this player"
    
    def set_role(self, Role):
        if self.role is None:
            self.role = Role

    def vote_player(self, name):
        self.last_voted = name
        return self.round, self.last_voted
    
# camp counsellor can look at 1 persons role at night
# have time state in gamestate
# get 2/3 unpicked roles from group
# 1 werewolf unless > 6
# 1 camp counsellor only if > 5 ppl

    

class GameState:
    def __init__(self, player_names, extra_roles=False):
        self.num_players = len(player_names)
        random_roles = self.set_random_roles(extra_roles)
        self.players = [Player(player_names[person], random_roles[person]) for person in range(self.num_players)]
        
    
    def set_random_roles(self, extra_roles):
        roles = {}
        
        if not extra_roles:
            for role in ROLE_INFO:
                if role['Required']:
                    roles[role]= ROLE_INFO[role]
        else: 
            roles = ROLE_INFO.copy()
        
        if self.num_players>5 and extra_roles:
            players_left = self.num_players
            role_limits = {"werewolf":2, "camp_councellor":1, "wannabe":1, "introvert":1, "bff_1":0, "bff_2":0, "camper":0,}
            players_left -= 4
            if players_left >= 2:
                role_limits['bff_1'] = 1
                role_limits['bff_2'] = 1
                players_left -= (role_limits['bff_1'] + role_limits['bff_2'])
            else:
                role_limits['camper'] = 1
                players_left -= role_limits['camper']          
            if players_left != 0:
                role_limits['camper'] += players_left
                players_left -= role_limits['camper']

            players = []
            for role in role_limits:
                limit = role_limits[role]
                while limit != 0:
                    players.append[role]
            random.shuffle(players)
            return players
        
        if self.num_players>5:
            pass
            
        return rand_roles
    
    def tally_votes(self):
        votes={}
        for player in self.players:
            if player.last_voted in votes:
                votes[player.last_voted] +=1
            else:
                votes[player.last_voted] = 1

        player_booted = max(votes, key=votes.get)
        return player_booted, votes[player_booted]

    
        

        
        
            
        


    
    
    



    