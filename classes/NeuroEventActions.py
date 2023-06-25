from classes.NeuroEventBot import NeuroEventBot

class Voting:
    def __init__(self, NEB: NeuroEventBot) -> None:
        self.NEB = NEB
    
    async def _send_list(voter_id: int, list_items: list[str]):
        pass
    
    async def send_lists_to_spectators(self, ctx):
        sm_id = self.NEB.spectators_msg_id
        if sm_id == None:
            raise ValueError('There is no msg id, where reactions can be obtained!')
        else:
            spectators_msg = await ctx.channel.fetch_message(sm_id)
            spectator_emoji_ind = 0 # i hope this is 0
            spectators = spectators_msg.reactions[spectator_emoji_ind].users()
    
    
    async def send_lists_to_artists(self):
        await self.NEB.fetch_user()
        for artist_id in self.NEB.state.art_dict:
            self.NEB.fetch_user()


    async def send_lists_to_organizers(self):
        pass