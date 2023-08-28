from discord.ext import commands
from classes.Texts import Texts
from classes.VoteList import ListCategory

class NeuroEventBot(commands.Bot):    
    spectators: list[int]
    
    art_dict: dict[str, str]
    top_lists: dict[int, dict[ListCategory, dict[int, str]]]
    
    def __init__(self, **args):
        super().__init__(command_prefix=Texts.PREFIX, **args)
        
        self.art_dict = {}
        self.spectators = []
        self.top_lists = {}
        
    async def setup_hook(self):
        await self.tree.sync()
        