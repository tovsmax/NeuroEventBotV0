from discord.ext.commands import Context
from discord import User
from classes.NeuroEventBot import NeuroEventBot

class Voting:
    def __init__(self, NEB: NeuroEventBot) -> None:
        self.NEB = NEB
    
    async def _send_list(self, voter: User, list_items: list[str]):
        msg_text = ', '.join(list_items)
        await voter.send(msg_text)
    
    async def send_lists_to_spectators(self, ctx: Context):
        sm_id = self.NEB.spectators_msg_id
        if sm_id == None:
            raise ValueError('There is no msg id, where reactions can be obtained!')
        else:
            spectators_msg = await ctx.channel.fetch_message(sm_id)
            spectator_emoji_ind = 0 # i hope this is 0
            spectators = spectators_msg.reactions[spectator_emoji_ind].users()
            spectators = [spectator async for spectator in spectators]
            
            for spectator in spectators[1:]:
                list_items = ['lol', 'kek']
                await self._send_list(spectator, list_items)
    
    
    async def send_lists_to_artists(self):
        await self.NEB.fetch_user()
        for artist_id in self.NEB.state.art_dict:
            self.NEB.fetch_user()


    async def send_lists_to_organizers(self):
        pass