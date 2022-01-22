ROLE_INFO = {"Werewolf": {"About": "see the other werewolves", "Required": True},
             "Camper": {"About": "we vibing fham", "Limit": 1000, "Required": True},
             "BFF-1": {"About": "half of best friends", "Limit": 1, "Required": False},
             "BFF-2": {"About": "other half of best friends", "Limit": 1, "Required": False},
             "Camp Counselor": {"About":"does counselling", "Limit": 1, "Required": False},
             "Wannabe": {"About": "does something", "Limit": 1, "Required": False},
             "Introvert": {"About": "we vibing fham 2.0", "Limit": 1, "Required": False}   
    
}


class GameState:
    def __init__(self, num_players):
        
        self.players = []
        pass


class Player:
    def __init__(self, role=None):
        self.role = role
    def get_role_info(self):
        pass
    def set_role(self, Role):
        if self.role is None:
            self.role = Role
    
    
    
    



    