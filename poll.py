import discord 
from globalvar import *

class poll:
    def __init__(self, user, emoji, voted="", votes=0):
        self.user = user     # name (string)
        self.emoji = emoji   # emoji
        self.voted = voted   # name
        self.votes = votes   # int

    def get_data(self):
        print(f'{self.user}+{self.emoji}j')

    def get_name_from_emoji(self, emoji):
        if self.emoji == emoji:
            return self.user
        else:
            return None
    
    def set_voted_for(self, user):
        self.voted = user
        return 


def create_poll(userlist, poll_list):
    embed = discord.Embed(
        title = "Who will you vote for?",
        description = "Choose who you want to send home tonight. You can only vote for one person! The most recent vote will be the one that's counted.",
        color = discord.Color.blue()
    )
    i = 0
    value = ""
    # For each player, add their name as an option
    while i < len(userlist):
        name = userlist[i].name
        emoji = unicode_letters[i]
        value = value + emoji + " " + name + "\n" 
        # update global variable poll_list, which maps emojis to names
        poll_list.append(poll(name, emoji))
        i = i+1
    
    embed.add_field(name = "Options", value = value)
    return embed