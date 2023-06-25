from discord.ext import commands
from classes.Texts import Texts
from classes.EventStage import EventStage

class NeuroEventBot(commands.Bot):
    def __init__(self, **args):
        super().__init__(command_prefix=Texts.PREFIX, **args)
        
        self.current_stage = EventStage.NOT_STARTED
        self.organizers = [
            252453718165815296, #petrarkius
        ]
        
        self.art_dict = {}
        self.spectators = []
        self.spectators_msg_id = None
        
    async def setup_hook(self):
        await self.tree.sync()