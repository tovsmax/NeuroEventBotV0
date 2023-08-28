from discord import Intents
import os

TOKEN = os.getenv('DISCORD_TOKEN')

intents = Intents.default()
intents.message_content = True
intents.members = True
intents.dm_messages = True


class Config:
    token = TOKEN
    intents = intents
