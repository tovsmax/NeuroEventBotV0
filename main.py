from discord.ext.commands import Context
from classes.Configuration import Config, Organizers
from classes.NeuroEventBot import NeuroEventBot
from classes.Texts import Texts
from classes.NeuroEventActions import Voting, Finishing
import re

if __name__ == '__main__':
    NEB = NeuroEventBot(intents=Config.intents)

    @NEB.hybrid_command()
    async def send_lists(ctx: Context, receivers: str, vote_items: str):
        if not Organizers().is_organizer(ctx.author.id):
            await ctx.reply(Texts.VOTING_NOT_ORGANIZER)
            return
        
        pattern = '<@(\d+)>'
        receiver_list = re.findall(pattern, receivers)
        vote_item_list = vote_items.split(', ')
        
        voting = Voting(NEB)
        
        for receiver in receiver_list:
            id = int(receiver)
            voter = NEB.get_user(id)
            await voting._send_list(voter, vote_item_list)
        
        await ctx.reply(Texts.VOTING_STARTED)
        
    @NEB.hybrid_command()
    async def get_total_scores(ctx: Context):
        pass
            
    NEB.run(Config.token)

