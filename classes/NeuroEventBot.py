from discord.ext import commands
from classes.Texts import Texts
from classes.EventStage import EventStage
from classes.VoteList import ListCategory

class NeuroEventBot(commands.Bot):
    current_stage: EventStage
    spectators: list[int]
    spectators_msg_id: int
    
    organizers: list[int]
    art_dict: dict[str, str]
    art_top: dict[str, dict[str, int]]
    top_lists: dict[int, dict[ListCategory, dict[int, str]]]
    
    
    
    def __init__(self, **args):
        super().__init__(command_prefix=Texts.PREFIX, **args)
        
        self.current_stage = EventStage.NOT_STARTED
        self.organizers = [
            252453718165815296, #petrarkius
        ]
        
        self.art_dict = {}
        self.spectators = []
        self.spectators_msg_id = None
        self.art_top = {}
        self.top_lists = {}
        
    async def setup_hook(self):
        await self.tree.sync()