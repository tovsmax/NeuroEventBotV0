from typing import Union
from discord.ext import commands
from classes.Texts import Texts
from classes.EventStage import EventStage
from classes.VoteList import ListCategory
from discord.ext.commands import Context
from discord import User, Member

class NeuroEventBot(commands.Bot):
    current_stage: EventStage
    spectators: list[int]
    spectators_msg_id: int
    
    organizers: list[int]
    art_dict: dict[str, str]
    # art_top: dict[str, dict[str, int]]
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
        # self.art_top = {}
        self.top_lists = {}
        
    async def setup_hook(self):
        await self.tree.sync()
    
    async def _get_gathering_spectators_msg(self, ctx: Context):
        sm_id = self.spectators_msg_id
        if sm_id == None:
            raise ValueError('There is no msg id, where reactions can be obtained!')
        
        spectators_msg = await ctx.channel.fetch_message(sm_id)
        return spectators_msg
    
    async def get_spectators(self, ctx: Context) -> list[Union[User, Member]]:
        spectators_msg = self._get_gathering_spectators_msg(ctx)
        SPECTATOR_EMOJI_IND = 0
        spectators_async_iter = spectators_msg.reactions[SPECTATOR_EMOJI_IND].users()
        spectators = [
            spectator 
            async for spectator in spectators_async_iter 
            if spectator.id not in self.art_dict
        ]
        
        return spectators
    
    def get_artists(self):
        return list(self.art_dict.keys())
        