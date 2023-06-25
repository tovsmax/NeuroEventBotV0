from dotenv import load_dotenv
import os
from discord import Intents
from classes.NeuroEventBot import run_bot

if __name__ == '__main__':
    load_dotenv()

    TOKEN = os.getenv('DISCORD_TOKEN')

    intents = Intents.default()
    intents.message_content = True
    intents.members = True
    intents.dm_messages = True
    
    run_bot(intents, TOKEN)