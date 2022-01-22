import discord 
unicode_letters = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮"]

class poll:
    def __init__(self, user='0', votes=0):
        self.user = user
        self.votes = votes

    def get_data(self):
        print(f'{self.real}+{self.imag}j')



    def create_poll(self, userlist):
            embed = discord.Embed(
                title = "Who will you vote for?",
                description = "Choose who you want to send home tonight. You can only vote for one person!",
                color = discord.Color.blue()
            )
            i = 0
            while i < len(userlist):
                name = userlist[i].name
                emoji = unicode_letters[i]
                embed.add_field(name = name, value = emoji)
            return embed
