import discord 
class poll:
    def __init__(self, user, emoji, votes=0):
        self.user = user
        self.emoji = emoji
        self.votes = votes

    def get_data(self):
        print(f'{self.user}+{self.emoji}j')

    def get_name_from_emoji(self, emoji):
        if self.emoji == emoji:
            return self.user
        else:
            return None

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