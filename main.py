from discord.ext.commands import Context
from classes.Configuration import Config
from classes.NeuroEventBot import NeuroEventBot
from classes.Texts import Texts
from classes.NeuroEventActions import Voting, Finishing
import re

if __name__ == '__main__':
    NEB = NeuroEventBot(intents=Config.intents)

    @NEB.hybrid_command()
    async def send_lists(ctx: Context, receivers: str, vote_items: str):
        pattern = '<@(\d+)>'
        receiver_list = re.findall(pattern, receivers)
        vote_item_list = vote_items.split(', ')
        
        voting = Voting(NEB)
        
        for receiver in receiver_list:
            id = int(receiver)
            voter = NEB.get_user(id)
            await voting._send_list(voter, vote_item_list)
        
        print(NEB.top_lists)
        
        await ctx.reply(Texts.VOTING_STARTED)
        
    @NEB.hybrid_command()
    async def get_total_scores(ctx: Context):
        pass
            
    NEB.run(Config.token)

