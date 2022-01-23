import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event

async def on_message(message):
    emoji = '✅'
    if message.content == 'React to join game! Starting in 3 seconds...':
        await message.add_reaction(emoji)

client.run(TOKEN)