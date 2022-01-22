import random

ROLE_INFO = {"Werewolf": {"About": "see the other werewolves", "Required": True},
             "Camper": {"About": "we vibing fham", "Limit": 1000, "Required": True},
             "BFF-1": {"About": "half of best friends", "Limit": 1, "Required": False},
             "BFF-2": {"About": "other half of best friends", "Limit": 1, "Required": False},
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
    

class GameState:
    def __init__(self, player_names):
        self.num_players = len(player_names)
        random_roles = self.set_random_roles()
        self.players = [Player(player_names[person], random_roles[person]) for person in range(self.num_players)]
        
    
    def set_random_roles(self):
        rand_roles = ROLE_INFO.keys()
        random.shuffle(rand_roles)
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

    
        

        
        
            
        


    
    
    



    