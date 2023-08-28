from discord import Intents
import os
import json

TOKEN = os.getenv('DISCORD_TOKEN')

intents = Intents.default()
intents.message_content = True
intents.members = True
intents.dm_messages = True


class Config:
    token = TOKEN
    intents = intents


    
class Organizers:
    organizers: list[int]
    
    def __init__(self) -> None:
        with open('organizers.json') as orgs_file:
            self.organizers = json.load(orgs_file).values()
    
    def is_organizer(self, user_id: int):
        if user_id in self.organizers:
            return True
        return False
